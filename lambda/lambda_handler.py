from __future__ import print_function
import os
from random import randint
import mastodon_functions

# --------------- AVSへ返すJSONデータを生成するヘルパー関数 --------------------

def build_speechlet_response(title, output, reprompt_text, end_session):
    ''' インターフェースに直接関わる部分のデータを生成する関数 '''
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': end_session
    }


def build_response(session_attributes, speechlet_response):
    ''' インターフェースデータにセッションアトリビュートを加えて整形する関数 '''
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def build_toot_text(toot_json):
    ''' 入力したつぶやきのデータを整形する関数 '''

    # アカウント名とつぶやきの結合
    toot_text = ''
    for toot in toot_json:
        toot_text = '{}{}さん。{}。'.format(
            toot_text, toot['account'], toot['content'])
    # 4500文字を超えた場合
    if len(toot_text) > 4500:
        limit_comment =  '一度に読み上げられる数を超えてしまいました。'
        toot_text = '{}。{}'.format(toot_text[0:4400], limit_comment)

    return toot_text

# ---------------------- スキルの動作を制御する関数 ----------------------------

def GreetingTootIntent(intent):
    ''' 挨拶をつぶやく場合 '''

    # マストドンにつぶやく処理
    greet_msg = intent['slots']['greeting']['value']
    try:
        mstdn = mastodon_functions.mastodon(
            os.environ['FQDN'],
            os.environ['ACCESS_TOKEN']
        )

        # 挨拶の中身が無い場合
        toot_name = ['つぶやいて', 'つぶやく', 'つぶやき']
        if greet_msg in toot_name:
            toot_text = 'こんにちは'
        else:
            toot_text = greet_msg

        mstdn.toot(toot_text)
    except:
        return UnknownError()

    # AVSに返す情報の生成
    title = 'マストドン'
    approvel = [
        'わかりました。',
        '承知しました。',
        'OKです。',
        'もちろんです。',
        'かしこまりました。',
        '喜んで。'
    ]
    commnets = [
        f'「{toot_text}」とつぶやきました。',
        f'「{toot_text}」とつぶやいておきました。',
        f'「{toot_text}」とトゥートしました。',
        f'「{toot_text}」とトゥートしておきました。',
        f'「{toot_text}」とマストドンにトゥートしました。'
    ]
    next_comment = '次はどうしますか？'
    r1 = randint(0, len(approvel)-1)
    r2 = randint(0, len(commnets)-1)
    output = approvel[r1] + commnets[r2] + next_comment
    reprompt_text = next_comment
    end_session = False
    session_attributes = {'previous_intent': 'toot'}
    speechlet = build_speechlet_response(
        title, output, reprompt_text, end_session)

    return build_response(session_attributes, speechlet)


def TimeLineIntent_htl(intent):
    ''' ホームタイムラインを読み上げる場合 '''

    # マストドンからホームタイムラインのつぶやきを収集、整形する
    try:
        mstdn = mastodon_functions.mastodon(
            os.environ['FQDN'],
            os.environ['ACCESS_TOKEN']
        )
        toot_text = build_toot_text(mstdn.get_home_timeline())
    except:
        return UnknownError()

    # AVSに返す情報の生成
    title = 'マストドン'
    approvel = [
        'わかりました。',
        '承知しました。',
        'OKです。',
        'もちろんです。',
        'かしこまりました。',
        '喜んで。'
    ]
    commnets = [
        'それでは読み上げますね。',
        '今のトゥートはこんな感じです。',
        '直近のつぶやきはこんな感じです',
        '直近のつぶやきを読み上げます。',
        'ホームタイムラインでは次のようにつぶやかれています。'
    ]
    next_comment = '以上です。次はどうしますか？'
    r1 = randint(0, len(approvel)-1)
    r2 = randint(0, len(commnets)-1)
    output = approvel[r1] + commnets[r2] + toot_text + next_comment
    reprompt_text = '次はどうしますか？'
    end_session = False
    session_attributes = {'previous_intent': 'htl'}
    speechlet = build_speechlet_response(
        title, output, reprompt_text, end_session)
    return build_response(session_attributes, speechlet)


def TimeLineIntent_ltl(intent):
    ''' ローカルタイムラインを読み上げる場合 '''

    # マストドンからホームタイムラインのつぶやきを収集、整形する
    try:
        mstdn = mastodon_functions.mastodon(
            os.environ['FQDN'],
            os.environ['ACCESS_TOKEN']
        )
        toot_text = build_toot_text(mstdn.get_local_timeline())
    except:
        return UnknownError()

    # AVSに返す情報の生成
    title = 'マストドン'
    approvel = [
        'わかりました。',
        '承知しました。',
        'OKです。',
        'もちろんです。',
        'かしこまりました。',
        '喜んで。'
    ]
    commnets = [
        'それでは読み上げますね。',
        '今のトゥートはこんな感じです。',
        '直近のつぶやきはこんな感じです',
        '直近のつぶやきを読み上げます。',
        'ローカルタイムラインでは次のようにつぶやかれています。'
    ]
    next_comment = '以上です。次はどうしますか？'
    r1 = randint(0, len(approvel)-1)
    r2 = randint(0, len(commnets)-1)
    output = approvel[r1] + commnets[r2] + toot_text + next_comment
    reprompt_text = '次はどうしますか？'
    end_session = False
    session_attributes = {'previous_intent': 'ltl'}
    speechlet = build_speechlet_response(
        title, output, reprompt_text, end_session)

    return build_response(session_attributes, speechlet)


def NotificationIntent(intent):
    ''' 通知からメンションやダイレクトメッセージを読み上げる場合 '''

    # マストドンからメンションを収集、整形する
    toot_text = ''
    try:
        mstdn = mastodon_functions.mastodon(
            os.environ['FQDN'],
            os.environ['ACCESS_TOKEN']
        )
        toot_text = build_toot_text(mstdn.get_notification())
    except:
        UnknownError()

    # AVSに返す情報の生成
    title = 'マストドン'
    approvel = [
        'わかりました。',
        '承知しました。',
        'OKです。',
        'もちろんです。',
        'かしこまりました。',
        '喜んで。'
    ]
    commnets = [
        'それでは読み上げますね。',
        'こんなメンションやDMが届いています。',
        '直近のメンションやダイレクトメッセージはこんな感じです',
        '直近のメンションやDMを読み上げます。',
        '次のようなメンションやDMが届いています。'
    ]

    next_comment = '以上です。次はどうしますか？'
    r1 = randint(0, len(approvel)-1)
    r2 = randint(0, len(commnets)-1)
    output = approvel[r1] + commnets[r2] + toot_text + next_comment
    reprompt_text = '次はどうしますか？'
    end_session = False
    session_attributes = {'previous_intent': 'notify'}
    speechlet = build_speechlet_response(
        title, output, reprompt_text, end_session)

    return build_response(session_attributes, speechlet)


def RepeatIntent(intent, session):
    ''' 前のインテントの処理を繰り返す場合 '''
    previous_intent = session['attributes']['previous_intent']

    if previous_intent == 'toot':
        return GreetingTootIntent(intent)

    elif previous_intent == 'htl':
        return TimeLineIntent_htl(intent)

    elif previous_intent == 'ltl':
        return TimeLineIntent_ltl(intent)

    elif previous_intent == 'notify':
        return NotificationIntent(intent)

    else:
        UnknownIntent()


def UnknownError():
    ''' 不明なエラー処理が発生した場合 '''
    title = 'マストドン'
    commnets = [
        'すいません、ちょっとエラーが発生したっぽいので中止します。',
        '申し訳ありませんが、エラーが発生したのでやめました。',
        'はい、エラーです。ちょっとやめておきますね。'
        'エラーがありましたので、中断しました。ごめんなさい。'
        'すみません。エラーが発生しました。あとでもう一回試してみてくださいね。'
    ]
    reprompt_text = next_comment = '次はどうしますか？'
    output = commnets[randint(0, len(commnets)-1)] + next_comment
    end_session = False
    speechlet = build_speechlet_response(title, output, reprompt_text, end_session)

    return build_response({}, speechlet)


def UnknownIntent():
    ''' よくわからないインテントを受けつけた場合 '''
    title = 'マストドン'
    commnets = [
        'すいません、たぶんその機能はもってません。開発者にリクエストしてくださいね。',
        '申し訳ありませんが、知らない機能かもです',
        '私の知らない機能です。まだ実装してないかも。'
        'その機能って何ですか？もしよければ開発者にリクエストしてください。'
        'それは私の知らない機能です。今後は実装するかもしれませんので、お待ちください。'
    ]
    reprompt_text = next_comment = '次はどうしますか？'
    output = commnets[randint(0, len(commnets)-1)] + next_comment
    end_session = False

    return build_speechlet_response(title, output, reprompt_text, end_session)


def HelpIntent():
    ''' 使い方がわからない場合 '''
    title = 'マストドンの使い方'
    commnets = 'このスキルの機能は3つです。挨拶をつぶやく、タイムラインのつぶやくを聞く、あなた宛のメンション内容を聞く。'
    reprompt_text = next_comment = 'まずはタイムライン聞かせて、と言ってみて下さい'
    output = commnets + next_comment
    end_session = False

    return build_speechlet_response(title, output, reprompt_text, end_session)

# -------------------------- イベント関数 -----------------------------


def on_launch():
    ''' 特に指定なく呼び出された時の処理 '''
    title = 'マストドン'
    start_greeting = [
        'マストドンで何をしますか？',
        'マストドンで何したいですか？',
        '今日はマストドンで何をしますか？',
        '今日はマストドンで何したいですか？',
        'マストドンスキルです。何しますか？'
    ]
    output = start_greeting[randint(0, len(start_greeting)-1)]
    reprompt_text = 'マストドンで何しましょうか？'
    end_session = False
    speechlet = build_speechlet_response(title, output, reprompt_text, end_session)

    return build_response({}, speechlet)


def on_intent(intent_request, session):
    ''' インテントが指定された場合 '''

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # 呼び出されたインテントごとに処理を分配する
    if intent_name == "GreetingTootIntent":
        ''' つぶやきたい場合 '''
        return GreetingTootIntent(intent)

    elif intent_name == "TimeLineIntent":
        tl = intent["slots"]["timeline"]["resolutions"]['resolutionsPerAuthority'][0]['values'][0]['value']['id']
        if tl == 'HomeTimeLine':
            ''' ホームタイムラインが聞きたい場合 '''
            return TimeLineIntent_htl(intent)
        else:
            ''' ローカルタイムラインが聞きたい場合 '''
            return TimeLineIntent_ltl(intent)

    elif intent_name == "NotificationIntent":
        ''' メンションやダイレクトメッセージを聞きたい場合 '''
        return NotificationIntent(intent)

    elif intent_name == "AMAZON.RepeatIntent":
        ''' タイムラインの読み上げや通知を繰り返す場合 '''
        return RepeatIntent(intent, session)

    elif intent_name == "AMAZON.HelpIntent":
        ''' 使い方がわからない場合 '''
        return HelpIntent()

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        ''' キャンセルもしくは停止する場合 '''
        return handle_session_end_request()

    else:
        ''' よくわからない場合 '''
        return UnknownIntent()


def handle_session_end_request():
    ''' セッション終了する場合 '''

    card_title = "マストドン終了"
    speech_output = "マストドンを終わります。良いマストドンライフを！"
    end_session = True
    speechlet = build_speechlet_response(
        card_title, speech_output, None, end_session)

    return build_response({}, speechlet)


def handler(event, context):
    ''' AVSからキックされる処理 '''

    if event['request']['type'] == "LaunchRequest":
        return on_launch()

    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])

    elif event['request']['type'] == "SessionEndedRequest":
        return handle_session_end_request()

