"""Module to upload the report to Slack."""

from typing import cast

from packages.valory.protocols.http.message import HttpMessage
from packages.valory.connections.http_client.connection import PUBLIC_ID as HTTP_CLIENT_PUBLIC_ID, HttpDialogue


class Uploader:
    """Abstract class for uploading data to some destination."""

    def upload(self, dialogues, *args, **kwargs):
        """Upload data to some destination."""
        del args, kwargs, dialogues
        raise NotImplementedError


class SlackUploader(Uploader):
    """Uploads data to Slack."""

    token: str
    channel: str
    enabled: bool
    agent_address: str

    def __init__(self, **kwargs):
        """Initialize the uploader."""
        self.token = kwargs.pop("token")
        self.channel = kwargs.pop("channel")
        self.enabled = kwargs.pop("enabled")
        self.agent_address = kwargs.pop("agent_address")

    def upload(  # pylint: disable=W0221
        self,
        http_dialogues,
        data,
        file_name,
    ) -> None:
        """Upload data to some destination."""
        url = "https://slack.com/api/files.upload"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # the breifcase emoji in unicode
        csv_content = "\n".join(",".join(map(str, row)) for row in data)

        msg = f"Report for {file_name} is attached 💼"
        data = {
            "channels": self.channel,
            "initial_comment": msg,
            "content": csv_content,
            "filename": f"{file_name}.csv",
            "filetype": "csv",
        }
        header_string = ""
        for key, val in headers.items():
            header_string += f"{key}: {val}\r\n"

        data_string = ""
        for key, val in data.items():
            data_string += f"{key}={val}&"
        data_string = data_string[:-1]

        request_http_message, http_dialogue = http_dialogues.create(
            counterparty=str(HTTP_CLIENT_PUBLIC_ID),
            performative=HttpMessage.Performative.REQUEST,
            method="POST",
            url=url,
            headers=header_string,
            version="",
            body=data_string.encode("utf-8"),
        )
        request_http_message = cast(HttpMessage, request_http_message)
        http_dialogue = cast(HttpDialogue, http_dialogue)
        return request_http_message, http_dialogue
