# captionbot

## Usage

```python
>>> from captionbot import CaptionBot
>>> bot = CaptionBot()
>>> caption = bot.from_url(image_url="https://www.captionbot.ai/images/6.jpg")
>>> caption.text
"I think it's a man flying through the air while riding a skateboard. "
>>> caption2 = bot.from_file(filename="6.jpg")
>>> caption2.text
"I think it's a man flying through the air while riding a skateboard. "
```
