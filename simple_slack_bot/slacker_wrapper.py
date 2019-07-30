from slacker import Chat
import json


class SlackerWrapper(Chat):
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
                             'mrkdwn': True
                         })

    def me_message(self, channel, text):
        return self.post('chat.meMessage',
                         data={'channel': channel, 'text': text})

    def reply(self, channel, text=None, thread_ts=None,
              username=None, as_user=None, parse=None, link_names=None,
              attachments=None, unfurl_links=None, unfurl_media=None,
              icon_url=None, icon_emoji=None):

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
                             'thread_ts': thread_ts,
                             'icon_emoji': icon_emoji,
                             'as_user': True,
                             'link_names': 1
                         })
