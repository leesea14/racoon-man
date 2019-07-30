# Racoon Man
Simple Slack Bot Project **RACOON MAN**  
슬랙 봇 프로젝트 라쿤맨 입니다.    
Base Source : [https://github.com/GregHilston/Simple-Slack-Bot](https://github.com/GregHilston/Simple-Slack-Bot)  

추가/수정하고싶은 부분이 있다면 풀리퀘 날려주세요 🙆 

## Enviroment
python 3.6 이상

## Get Started
1. Install requirement
```
pip install -r requirement.txt
```

2. Create `.env` File
```
HERREN_TOKEN=YOUR_TOKEN
```

3. Run `example_component.py`

## Setting
slacker library `_init__.py`
Change this line.
```python
class Chat(BaseAPI):
    def post_message(self, channel, text=None, username=None, as_user=None,
                     parse=None, link_names=None, attachments=None,
                     unfurl_links=None, unfurl_media=None, icon_url=None,
                     icon_emoji=None):

        # Ensure attachments are json encoded
        if attachments:
            if isinstance(attachments, list):
                attachments = json.dumps(attachments)

        return self.post('chat.postMessage',
                         data={
                             'channel': channel,
                             'text': text,
                             'username': username,
                             'parse': 'full',
                             'attachments': attachments,
                             'unfurl_links': unfurl_links,
                             'unfurl_media': unfurl_media,
                             'icon_url': icon_url,
                             'icon_emoji': icon_emoji,
                             'as_user': True,
                             'link_names': 1,
                         })

```
