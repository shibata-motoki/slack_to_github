# coding: UTF-8
import requests
import json
import os

post_url = 'https://api.github.com/repos/<repo-owner-username>/<project-name>/pulls/<pull-number>/requested_reviewers?access_token=<personal-access-token-for-github>" -H "Content-Type: application/json" -X POST -d "{\"reviewers\":[\"reviewer1\"]}"'

curl "https://api.github.com/repos/<repo-owner-username>/<project-name>/pulls/<pull-number>/requested_reviewers?access_token=<personal-access-token-for-github>" -H "Content-Type: application/json" -X POST -d "{\"reviewers\":[\"reviewer1\"]}"

def post_slack(event, context, path):
     # slack送信
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
