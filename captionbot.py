import json
import mimetypes
from collections import namedtuple
from pathlib import Path
from typing import NamedTuple, Union

import requests

Caption = namedtuple("Caption", "text")


class CaptionBotAPI:
    def __init__(self) -> None:
        super(CaptionBotAPI, self).__init__()
        self._session = requests.session()

    def from_url(self, image_url: str) -> Union[NamedTuple, None]:
        """Build caption for a given URL"""
        url = "https://captionbot.azurewebsites.net/api/messages"
        querystring = {"language": "en-US"}
        headers = {"Content-Type": "application/json"}
        payload = {"Type": "CaptionRequest", "Content": image_url}

        response = self._session.post(
            url=url,
            data=json.dumps(obj=payload),
            headers=headers,
            params=querystring,
        )

        if not response.ok:
            return

        if response.text:
            caption = Caption(text=response.text)
            return caption

    def from_file(self, filename: str) -> Union[NamedTuple, None]:
        """Build caption for a given filename"""
        url = "https://www.captionbot.ai/api/upload"
        content_type, encoding = mimetypes.guess_type(url=filename)

        path = Path(filename)
        name = path.name
        files = {"file": (name, path.read_bytes(), content_type)}

        response = self._session.post(url=url, files=files)

        if not response.ok:
            return

        if response.text:
            # Remove double quotes from the URL
            image_url = response.text[1:-1]
            return self.from_url(image_url=image_url)
