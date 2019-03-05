import json
import logging

import requests

API_URL = "https://captionbot.azurewebsites.net/api/messages"


class Caption(object):
    def __init__(self):
        super(Caption, self).__init__()
        self.caption = None
        self.image_url = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.image_url, self.caption})"

    @classmethod
    def from_dict(klass, response, parser):
        c = klass()
        # Add the caption from the returned JSON object to instance.
        setattr(c, "caption", response.json())
        setattr(c, "image_url", response.request.body["Content"])

        return c


class CaptionBotAPI(object):
    def __init__(self):
        super(CaptionBotAPI, self).__init__()
        self._session = requests.session()

    def parse(self, image_url):
        querystring = {"language": "en-US"}
        headers = {"Content-Type": "application/json"}
        payload = {"Type": "CaptionRequest", "Content": image_url}

        try:
            r = self._session.post(
                url=API_URL,
                data=json.dumps(obj=payload),
                headers=headers,
                params=querystring,
            )
            r.raise_for_status()
        except Exception as exc:
            if hasattr(exc, "message"):
                logging.error(msg=f"{self.__class__.__name__}: {exc.message}")
            return

        caption = Caption.from_dict(response=r, parser=self)
        return caption
