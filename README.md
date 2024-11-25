# Hermes

Hermes is a versatile Discord bot designed to monitor specific channels for messages with attachments.
When it detects attachments, Hermes automatically uploads them to a configured Amazon S3 bucket.
The bot's configuration is fully customizable using environment variables, making it easy to deploy and adapt for
various use cases.

## Features

- **Channel Monitoring**: Observes specified Discord channels for messages.
- **Automated Uploads**: Automatically transfers detected attachments to an S3 bucket.
- **Configurable Setup**: Supports environment variables for dynamic configuration.
- **Docker Support**: Simplifies deployment with Docker and Docker Compose.

## Getting Started

### Cloning the Repository

Clone the Hermes repository to your local machine:

```bash
# Clone the repository
$ git clone https://github.com/NoahH99/hermes.git
$ cd hermes
```

### Configuration

Hermes requires environment variables for setup. Modify the docker-compose.yaml file directly. Below are the required
variables:

| Variables               | Description                                                                                                        |
|-------------------------|--------------------------------------------------------------------------------------------------------------------|
| `BOT_TOKEN`             | Your Discord bot token                                                                                             |
| `COMMAND_PREFIX`        | Prefix for bot commands (e.g., `!`).                                                                               |
| `BOT_ADMINISTRATORS`    | Comma-separated list of administrator Discord user IDs.                                                            |
| `S3_BUCKET_NAME`        | Name of the AWS S3 bucket for uploads.                                                                             |
| `AWS_REGION`            | AWS region of the S3 bucket.                                                                                       |
| `AWS_ACCESS_KEY_ID`     | Your AWS access key ID.                                                                                            |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret access key.                                                                                        |
| `WATCHED_CHANNELS`      | Comma-separated list of Discord server and channel IDs to monitor. (e.g., `000000000000000000:000000000000000000`) |
| `CDN_DOMAIN`            | Domain to serve uploaded files.                                                                                    |

### Running Locally

1. Build and start the Docker container:
    ```bash
    docker compose up --build
    ```
2. Hermes will start monitoring the specified channels and uploading attachments to the configured S3 bucket.

To run Hermes locally without Docker:

1. Install Python 3.9 or higher.
2. Create a virtual environment and install dependencies
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3. Set the environment variables (e.g., using a `.env` file).
4. Run the bot:
    ```bash
    python bot/bot.py
    ```

## Contributing

Contributions to the Hermes are welcome! If you find any issues or have suggestions for improvements, please
open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](/LICENSE).

```
MIT License

Copyright (c) 2024 Noah Hendrickson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
