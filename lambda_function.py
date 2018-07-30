# coding: UTF-8
import requests
import json
import os

post_url = 'https://hooks.slack.com/services/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'

def open_jsonfile(path):
    # json設定ファイル読み込み
    with open(path, 'r') as f:
        return json.loads(f.read())

def loads_githubwebhook():
    return open_jsonfile('sample.json')

"""
test = loads_githubwebhook()
#print(test)
event = test
context = 0
test2 = open_jsonfile('lambda.json')
print(test2['slackUsers'])
"""

def check_review_request(event):
    # ReviewRequestかどうかチェック
    if event.get('action') == 'review_requested':
        return True
    else:
        return False

def mapping_account(event):
    # githubとslackアカウントを紐づけ
    # jsonに名前がない場合、githubアカウントを返す
    github_name = event['pull_request']['requested_reviewers'][0]['login']
    slack_accounts = open_jsonfile('lambda.json')['slackUsers']
    return slack_accounts.get(github_name, 'githubname:'+github_name)

def slack_message(path):
    # slackに送信する内容
    return open_jsonfile(path)['message']['requestReview']

def get_review_url(event):
    # reviewするurlを取得
    return event['pull_request']['url']

def post_slack(event, context, path):
     # slack送信
     username = mapping_account(event)
     message = slack_message(path)
     url = get_review_url(event)
     requests.post(post_url, data = json.dumps({
            'text': '@{} {}\n{}'.format(username, message, url), # 投稿するテキスト
            'username': 'github', # 投稿のユーザー名
            'link_names': 1, # メンションを有効にする
            'channel': 'github_to_slack', # チャンネル
            'icon_emoji': 'icon', # アイコン
        }))

def lambda_handler(event, context):
    if check_review_request(event) is True:
        post_slack(event, context, 'lambda.json')
        return { 'statusCode': 200, 'body': json.dumps(event) }
    else:
        return { 'statusCode': 200, 'body': json.dumps(event) }

"""
lambda_handler(event, context)
"""
