from titan_apis import *

openai_functions = [
    {
        "name": "send_mail",
        "description": "send email to an email",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "email address to which email needs to be sent",
                },
                "subject": {
                    "type": "string",
                    "description": "Subject of the email",
                },
                "body": {
                    "type": "string",
                    "description": "Body of the email",
                }
            },
            "required": ["to", "subject", "body"],
        },
    },
    {
        "name": "search_email",
        "description": "search all the emails of the user to find specific email that user wants",
        "parameters": {
            "type": "object",
            "properties": {
                "from_email": {
                    "type": "string",
                    "description": "from email address which can be userd to filter all emails sent by a certain email address",
                },
                "words": {
                    "type": "string",
                    "description": "text which should be there in email subject or body",
                }
            },
            "required": ["from_email", "words"],
        },
    },
    {
        "name": "change_name",
        "description": "Change the name of the user to new specified name",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "new name of the user",
                },
            },
            "required": ["name"],
        },
    },
    {
        "name": "create_folder",
        "description": "create a new folder for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_name": {
                    "type": "string",
                    "description": "folder name which user wants to create",
                },
            },
            "required": ["folder_name"],
        },
    },
    {
        "name": "add_rule_move_to_folder",
        "description": "add a new filter or rule which helps user to to filter his incoming mails. For example move mails coming from certain email to some folder",
        "parameters": {
            "type": "object",
            "properties": {
                "rule_name": {
                    "type": "string",
                    "description": "name of the rule user wants to create",
                },
                "from_email": {
                    "type": "string",
                    "description": "a valid emaill address for the the filter being created. Filter will be applied on all the mail coming from this email",
                },
                "folder_name": {
                    "type": "string",
                    "description": "folder name to which mails need to be moved to based on the filter",
                }
            },
            "required": ["rule_name", "from_email", "folder_name"],
        }
    }
]


def send_mail_ai(args):
    send_mail(args['to'], args['subject'], args['body'])
    return "Mail has been sent. Reply to user with a done response. Dont reply with a function response"


def search_mail_ai(args):
    resp = search_email(args['from_email'], args['words'])
    if 't' in resp:
        emails_list = []
        for thread in resp['t'][:5]:
            mail = {'from': thread['tp']['from'][0]['email'],
                    'subject': thread['subject'],
                    'body_snippet': thread['snippet']
                    }
            emails_list.append(mail)
        return "Here is json list of found emails. Show to user in nice format. {}".format(emails_list)

    return "No Email were found"


def change_name_ai(args):
    change_name(args['name'])
    return "Name has been changed. Reply to user with a done response. Dont reply with a function response"


def create_folder_ai(args):
    create_folder(args['folder_name'])
    return "Folder has been created. Reply to user with a done response. Dont reply with a function response"


def create_rule_ai(args):
    add_rule_move_to_folder(
        args['rule_name'], args['from_email'], args['folder_name'])
    return "Rule has been created. Reply to user with a done response. Dont reply with a function response"


ai_python_mapping = {
    "send_mail": send_mail_ai,
    "search_email": search_mail_ai,
    "change_name": change_name_ai,
    "create_folder": create_folder_ai,
    "add_rule_move_to_folder": create_rule_ai,
}


def make_ai_function_call(ai_fn_str, args):
    print('making function call {} with args {}'.format(ai_fn_str, args))
    return ai_python_mapping[ai_fn_str](args=args)


if __name__ == '__main__':
    print(search_mail_ai({'from_email': 'luv@titan.email', 'words': 'Hi'}))
