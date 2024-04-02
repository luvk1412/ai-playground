# pip install Flask
# pip install openai
# python server.py

from flask import Flask, request, jsonify
from openai_helper import *
import json
import random
import string
from data_class import UserWebsiteInput


app = Flask(__name__)

threads = {}

def get_model_from_query_params(request):
    query_param = request.args.get('model', '3')
    if query_param == 3:
        return gpt3_model
    return gpt4_model

def raise_value_error_if_not(value, var_name, data_type):
    if value is None:
        raise ValueError(f'{var_name} expected but not present')
    if not isinstance(value, data_type):
        raise ValueError(f'{var_name} expected in {str(data_type)} format but received {str(type(value))}')
    
def generate_random_alphanumeric(length):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))

@app.errorhandler(Exception)
def handle_error(error):
    response = {
        'message': str(error),
        'type': type(error).__name__
    }
    if isinstance(error, ValueError):
        status_code = 400
    else:
        status_code = 500
    return jsonify(response), status_code


@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.json
    system_prompt = data.get('system_prompt')
    user_prompt = data.get('user_prompt')
    
    raise_value_error_if_not(value=system_prompt, var_name='system_prompt', data_type=str)
    raise_value_error_if_not(value=user_prompt, var_name='user_prompt', data_type=str)

    response = call_openai(conversation_history=get_new_conversation(system_prompt=system_prompt, user_prompt=user_prompt), output_json=True, model=get_model_from_query_params(request=request))
    return jsonify({'response': get_json_resp(openai_resp=response)})


@app.route('/create_website', methods=['POST'])
def create_website():
    data = request.json
    user_input = UserWebsiteInput(data)
    user_input.validate()
    
    landing_page, website_data = build_website(user_input=user_input, model=get_model_from_query_params(request=request))
    return jsonify({'landing_page': landing_page,  'website_data': website_data})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    user_message = data.get('user_message')
    website_data = data.get('website_data')
    
    raise_value_error_if_not(value=user_message, var_name='user_message', data_type=str)
    if thread_id:
        raise_value_error_if_not(value=thread_id, var_name='thread_id', data_type=str)
    else:
        raise_value_error_if_not(value=website_data, var_name='website_data', data_type=dict)



    get_next_chat_message()

    return jsonify({'response': get_json_resp(openai_resp=response)})

if __name__ == '__main__':
    app.run(debug=True)
