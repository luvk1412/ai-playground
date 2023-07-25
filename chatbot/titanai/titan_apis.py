import requests
import json
from dotenv import load_dotenv
import os
import random


load_dotenv()
env = os.getenv('ENV')
st = os.getenv('ST')
aid = os.getenv('aid')
mail_id = aid
email = os.getenv('email')


headers = {
    'content-type': 'application/json',
    'x-session-token': st,  # replace 'token' with your actual token
}

if env == 'prod':
    gateway_url = "https://api.flockmail.com/s/1002/{}/".format(aid)
    bll_url = "https://bll.titan.email/"
else:
    gateway_url = "https://flockmail-backend.flock-staging.com/s/1/{}/".format(
        aid)
    bll_url = "https://flockmail-bll.flock-staging.com/"


def send_mail(to, subject, body):
    url = gateway_url + 'v3/send/'
    data = {
        "crid": str(random.randint(1, 10000000)),
        "ctid": random.randint(1, 100000000),
        'flowId': str(random.randint(1, 10000000)),
        "sender": {
            "email": email
        },
        "subject": subject,
        "body": body,
        "to": [
            {
                "name": "",
                "email": to
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    resp_json = response.json()
    print(resp_json)
    return resp_json


def search_email(from_email=None, words=""):
    url = gateway_url + 'search'
    data = {
        "words": words
    }
    if from_email:
        data['from'] = [from_email]
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def change_name(name):
    url = bll_url + 'internal/email/set-config'
    data = {
        "accountId": aid,
        "name": name
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def create_folder(folder_name):
    url = gateway_url+'folders'
    data = {
        "folder_name": folder_name
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def add_rule_move_to_folder(rule_name, from_email, folder_name):
    exisitng_filters = get_mail_rules().get('filters')
    if not exisitng_filters:
        exisitng_filters = []
    print('got exisitng rules')
    new_rule = {
        "ruleName": rule_name,
        "conditions": [
            {
                "addressTypes": [
                    "From"
                ],
                "addresses": [
                    from_email
                ],
                "type": "address"
            }
        ],
        "actions": [
            {
                "folderName": folder_name,
                "type": "moveToFolder"
            }
        ]
    }

    exisitng_filters.append(new_rule)
    existing_folders = [f['name'] for f in get_mail_folders()['folders']]
    print('got exisitng folder')
    if folder_name not in existing_folders:
        print('creating new folder')
        create_folder(folder_name=folder_name)
        print('Created new folder')
    return update_mail_filters(exisitng_filters)


def update_mail_filters(filters):
    url = gateway_url + 'sieve/v4'
    data = {
        "filters": filters
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def get_mail_rules():
    url = gateway_url + 'sieve/v2/?partnerId=1'
    response = requests.get(url, headers=headers)
    return response.json()


def get_mail_folders():
    url = gateway_url + 'folders?crid=w_21104325_GFR_11_905_gxkb'
    response = requests.get(url, headers=headers)
    return response.json()


if __name__ == '__main__':
    print(email)
    print(search_email("luv@titan.email", "Hi"))
