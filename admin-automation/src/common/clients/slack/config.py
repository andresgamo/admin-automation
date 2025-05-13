import os
import base64
from typing import Optional, Dict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    """
    Simple Slack client for posting messages, uploading files, and sharing URLs.
    """

    def __init__(self, token: Optional[str] = None):
        token = token or os.getenv("SLACK_BOT_TOKEN")
        if not token:
            raise ValueError("SLACK_BOT_TOKEN environment variable is required")
        self.client = WebClient(token=token)

    def post_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[list] = None,
        attachments: Optional[list] = None,
    ) -> Dict:
        """
        Post a message to a Slack channel.
        """
        try:
            resp = self.client.chat_postMessage(
                channel=channel, text=text, blocks=blocks, attachments=attachments
            )
            return resp.data
        except SlackApiError as e:
            raise RuntimeError(
                f"Slack post_message error: {e.response['error']}"
            ) from e

    def upload_file(
        self,
        channel: str,
        file_bytes: bytes,
        filename: str,
        title: Optional[str] = None,
        initial_comment: Optional[str] = None,
    ) -> Dict:
        """
        Upload an in-memory file (e.g. PDF) to Slack.
        """
        try:
            resp = self.client.files_upload_v2(
                channel=channel,
                file=base64.b64decode(file_bytes),
                filename=filename,
                title=title,
                initial_comment=initial_comment,
            )
            return resp.data
        except SlackApiError as e:
            raise RuntimeError(f"Slack upload_file error: {e.response['error']}") from e
    def share_url(
        self,
        channel: str,
        url: str,
        title: Optional[str] = None,
        text: Optional[str] = None,
    ) -> Dict:
        """
        Share an external URL by posting a message with a link attachment.
        """
        attachment = [{"fallback": title or url, "title": title, "title_link": url}]
        return self.post_message(
            channel=channel, text=text or url, attachments=attachment
        )
