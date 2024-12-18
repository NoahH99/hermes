import json
import logging
import os

logger = logging.getLogger("config")


class Config:
    def __init__(self):
        self.version = self._get_version()

        secrets = json.loads(self._get_env("SECRETS", required=True))
        self.s3_bucket_name = secrets.get("S3_BUCKET_NAME")
        self.bot_token = secrets.get("BOT_TOKEN")

        self.command_prefix = self._get_env("COMMAND_PREFIX", default="!")
        self.bot_administrators = self._parse_admin_ids(self._get_env("BOT_ADMINISTRATORS", default=""))
        self.s3_region = self._get_env("AWS_REGION", "us-east-1")

        raw_watched_channels = self._get_env("WATCHED_CHANNELS", default="")
        self.watched_channels = self._parse_watched_channels(raw_watched_channels)

        self.cdn_domain = self._get_env("CDN_DOMAIN", required=True)

    @staticmethod
    def _get_env(var_name: str, default: str = None, required: bool = False):
        """
        Retrieve environment variables with optional validation.
        """
        value = os.getenv(var_name, default)

        if required and not value:
            raise ValueError(f"Environment variable '{var_name}' is required but not set.")

        return value

    @staticmethod
    def _parse_admin_ids(admin_ids: str):
        """
        Parse a comma-separated list of Discord admin IDs into a list of integers.
        """
        if not admin_ids:
            return []
        try:
            return [int(admin_id.strip()) for admin_id in admin_ids.split(",")]
        except ValueError:
            raise ValueError("BOT_ADMINISTRATORS must be a comma-separated list of valid Discord user IDs.")

    @staticmethod
    def _parse_watched_channels(raw_data: str):
        """
        Parse a string of guild:channel pairs into a validated dictionary.
        Example input: "12345:67890,23456:78901"
        Output: {12345: [67890], 23456: [78901]}
        """
        guild_channels = {}

        if not raw_data:
            return guild_channels

        try:
            for pair in raw_data.split(","):
                guild_id, channel_id = map(int, pair.split(":"))

                if guild_id not in guild_channels:
                    guild_channels[guild_id] = []

                guild_channels[guild_id].append(channel_id)
        except ValueError:
            raise ValueError(
                "GUILD_CHANNELS must be a comma-separated list of guild:channel pairs, e.g., '12345:67890,23456:78901'."
            )

        return guild_channels

    @staticmethod
    def _get_version():
        version_file = os.path.join(os.path.dirname(__file__), "version.txt")

        if os.path.exists(version_file):
            with open(version_file, "r") as version_file:
                return version_file.read().strip()

        return "unknown"

    def validate(self):
        """
        Perform additional validation on parsed config if necessary.
        """
        if not self.watched_channels:
            logger.warning("No guild:channel mappings provided. Bot will not handle any messages.")
        if not self.bot_administrators:
            logger.warning("No bot administrators specified. Admin commands will be inaccessible.")
