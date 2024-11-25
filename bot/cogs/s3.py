import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple

import boto3
import humanize
from discord import Message, Attachment, CustomActivity
from discord.ext import commands

from config import Config

logger = logging.getLogger("s3.cog")


class UploadToS3(commands.Cog):
    """
    Discord bot cog for handling file uploads to an S3 bucket.
    """

    FILE_TYPES: Dict[str, List[str]] = {
        "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"],
        "documents": [".pdf", ".doc", ".docx", ".txt", ".csv", ".xlsx"],
        "videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "audio": [".mp3", ".wav", ".aac", ".flac"],
        "archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    }

    def __init__(self, bot: commands.Bot, config: Config):
        self.bot = bot
        self.config = config
        self.cdn_domain = self.config.cdn_domain

        self.s3_client = boto3.client(
            "s3",
            region_name=self.config.s3_region,
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key,
        )

    def calculate_bucket_stats(self) -> Tuple[int, int]:
        """
        Calculate the total number of files and total size in the S3 bucket.

        Returns:
            Tuple[int, int]: Total file count and total size in bytes.
        """
        bucket_name = self.config.s3_bucket_name
        paginator = self.s3_client.get_paginator("list_objects_v2")
        total_size = 0
        total_files = 0

        for page in paginator.paginate(Bucket=bucket_name):
            if "Contents" in page:
                for obj in page["Contents"]:
                    total_files += 1
                    total_size += obj["Size"]

        return total_files, total_size

    async def update_presence(self) -> None:
        """
        Periodically update the bot's presence with the total number of files
        and the total size of files in the S3 bucket.
        """
        try:
            total_files, total_size = self.calculate_bucket_stats()
            humanized_size = humanize.naturalsize(total_size, binary=True)
            activity_text = f"{total_files} files ({humanized_size})"

            await self.bot.change_presence(activity=CustomActivity(f"Managing {activity_text}"))

            logger.info(f"Updated presence to: {activity_text}")
        except Exception as e:
            logger.error(f"Failed to update presence: {e}")

    async def delayed_update_presence(self):
        """
        Delay updating the bot's presence by 30 seconds.
        """
        await asyncio.sleep(45)
        await self.update_presence()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Wait until the bot is fully initialized before starting the background task.
        """
        await self.update_presence()

    def is_watched_channel(self, guild_id: int, channel_id: int) -> bool:
        """
        Check if a given guild and channel ID combination is monitored.
        """
        return (
                guild_id in self.config.watched_channels
                and channel_id in self.config.watched_channels[guild_id]
        )

    async def process_attachments(self, attachments: List[Attachment], channel):
        """
        Process and upload attachments to S3, and notify the user of the outcome.
        """
        for attachment in attachments:
            public_url = await self.upload_to_s3(attachment)

            try:
                if public_url:
                    await channel.send(f"File uploaded successfully: {public_url}")
            except Exception as e:
                await channel.send(f"File upload failed: {str(e)}")
                logger.error(f"Failed to upload {attachment.filename} to S3: {str(e)}", exc_info=True)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """
        Listener for Discord messages. Processes file uploads to S3.
        """
        if message.author.bot:
            return

        guild_id = message.guild.id if message.guild else None
        channel_id = message.channel.id if message.channel else None

        if not guild_id or not channel_id:
            logger.debug("Message ignored (no guild/channel context).")
            return

        if not self.is_watched_channel(guild_id, channel_id):
            logger.debug("Message ignored (not in monitored guild/channel).")
            return

        logger.info(f"Processing message from guild {guild_id}, channel {channel_id}.")
        await self.process_attachments(message.attachments, message.channel)
        asyncio.create_task(self.delayed_update_presence())

    def determine_file_type(self, file_extension: str) -> str:
        """
        Determine the category of a file based on its extension.
        """
        for category, extensions in self.FILE_TYPES.items():
            if file_extension in extensions:
                return category

        return "files"

    def check_and_rename_key(self, base_key: str) -> str:
        """
        Check if a key exists in S3 and rename it if necessary to avoid duplicates.
        """
        counter = 1
        key = base_key

        while True:
            try:
                self.s3_client.head_object(Bucket=self.config.s3_bucket_name, Key=key)
                base, ext = os.path.splitext(base_key)
                key = f"{base}-{counter}{ext}"
                counter += 1
            except self.s3_client.exceptions.ClientError as e:
                if "Not Found" in str(e):
                    return key
                else:
                    raise e

    def generate_unique_key(self, file_type: str, filename: str) -> str:
        """
        Generate a unique S3 key for the file based on its type and timestamp.
        """
        now = datetime.now(timezone.utc)
        year, month = now.year, now.month
        base_key = f"{file_type}/{year}/{month}/{filename}"

        return self.check_and_rename_key(base_key)

    def build_s3_put_params(self, unique_key: str, file_data: bytes, content_type: Optional[str]) -> Dict[str, any]:
        """
        Build parameters for the S3 put_object method.
        """
        params = {
            "Bucket": self.config.s3_bucket_name,
            "Key": unique_key,
            "Body": file_data,
            "ContentDisposition": "inline",
        }

        if content_type:
            params["ContentType"] = content_type

        return params

    async def upload_to_s3(self, attachment: Attachment) -> str:
        """
        Upload an attachment to the S3 bucket and return its public URL.
        """
        file_extension = os.path.splitext(attachment.filename)[-1].lower()
        file_type = self.determine_file_type(file_extension)

        unique_key = self.generate_unique_key(file_type, attachment.filename)
        file_data = await attachment.read()

        put_object_params = self.build_s3_put_params(unique_key, file_data, attachment.content_type)
        self.s3_client.put_object(**put_object_params)

        public_url = f"https://{self.cdn_domain}/{unique_key}"
        logger.info(f"Uploaded {attachment.filename} to S3 (key: {unique_key}).")

        return public_url


async def setup(bot: commands.Bot):
    """
    Setup function to add the cog to the bot.
    """
    await bot.add_cog(UploadToS3(bot, bot.config))
