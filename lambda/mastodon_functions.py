from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
import re
import json
import emoji

class mastodon:
    def __init__(self, fqdn, access_token):
        self.fqdn = fqdn
        self.access_token = access_token
        self.header = {'Authorization': 'Bearer ' + access_token}

    def remove_emoji(self, src_str):
        ''' 絵文字を全て駆逐するクラス内処理向けの関数 '''
        return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

    def get_text_only(self, content):
        ''' つぶやき内容を整形するクラス内処理向けの関数 '''
        text = self.remove_emoji(content)
        text = re.sub(r"<[^>]*?>", "", text)
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
        text = re.sub(r"#([\w]+)", "", text)
        return text

    def get_notify_text_only(self, content):
        ''' 通知のつぶやき内容を整形するクラス内処理向けの関数 '''
        text = self.get_text_only(content)
        text = re.sub(r"@([\w]+)", "", text)
        return text

    def toot(self, text):
        ''' つぶやく関数 '''
        _request = Request(
            url=f'https://{self.fqdn}/api/v1/statuses',
            headers=self.header
        )
        _post_data = urlencode({"status": text}).encode("utf-8")

        try:
            with urlopen(_request, _post_data) as _res:
                return json.loads(_res.read().decode('utf-8'))
        except HTTPError as _err:
            raise(_err.code)
        except URLError as _err:
            raise(_err.code)

    def get_timeline(self, req_url):
        ''' タイムラインを古い順に20件取得する関数 '''
        # タイムラインを取得する
        _request = Request(
            url=req_url,
            headers=self.header
        )
        try:
            with urlopen(_request) as _res:
                _toots = json.loads(_res.read().decode('utf-8'))
        except HTTPError as err:
            raise err.code
        except URLError as err:
            raise err.code

        # JSON形式でアカウント名と内容のみに絞る
        _res_toot = []
        for _toot_json in _toots:
            account = _toot_json['account']['display_name']
            content = _toot_json['content']
            _res_toot.append({
                'account': self.remove_emoji(account),
                'content': self.get_text_only(content)
            })

        # 古い順につぶやきを並べ直す
        _res_toot.reverse()

        return(_res_toot)

    def get_home_timeline(self):
        ''' ホームタイムラインのつぶやきを20件取得する関数 '''
        _url = f'https://{self.fqdn}/api/v1/timelines/home?limit=20'
        return self.get_timeline(_url)

    def get_local_timeline(self):
        ''' ローカルタイムラインのつぶやきを20件取得する関数 '''
        _url = f'https://{self.fqdn}/api/v1/timelines/public?local=yes&limit=20'
        return self.get_timeline(_url)

    def get_notification(self):
        ''' 通知からメンションとダイレクトメッセージだけ20件取得する関数 '''
        # メンションとダイレクトメッセージを取得する
        _url = f'https://{self.fqdn}/api/v1/notifications?exclude_types[]=follow&exclude_types[]=favourite&exclude_types[]=reblog&limit=20'
        _request = Request(
            url=_url,
            headers=self.header
        )
        try:
            with urlopen(_request) as _res:
                _toots = json.loads(_res.read().decode('utf-8'))
        except HTTPError as err:
            return err.code
        except URLError as err:
            return err.code

        # JSON形式でアカウント名と内容のみに絞る
        _res_toot = []
        for _toot_json in _toots:
            account = _toot_json['account']['display_name']
            content = _toot_json['status']['content']
            _res_toot.append({
                'account': self.remove_emoji(account),
                'content': self.get_notify_text_only(content)
            })

        # 古い順につぶやきを並べ直す
        _res_toot.reverse()

        return(_res_toot)
