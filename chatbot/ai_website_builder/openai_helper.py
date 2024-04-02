from openai import OpenAI
from constants import website_json_format
from data_class import UserWebsiteInput
import json

client = OpenAI(api_key="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")
gpt3_model = "gpt-3.5-turbo-0125"
gpt4_model = "gpt-4-0125-preview"

def call_openai(conversation_history, output_json=False, functions=None, model=gpt3_model, temperature=1):
    response_format = {"type": "text"}
    tools = []
    if output_json:
        response_format["type"] = "json_object"
    if functions:
        for function in functions:
            tools.append({
                "type": "function",
                "function": function
            })
    if tools:
        return client.chat.completions.create(model=model, response_format=response_format, messages=conversation_history, tools=tools, temperature=temperature)
    return client.chat.completions.create(model=model, response_format=response_format, messages=conversation_history, temperature=temperature)


def get_new_conversation(system_prompt, user_prompt):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def add_assistant_message(message, conversation):
    conversation.append({"role": "assistant", "content": message})
    return conversation

def add_user_message(message, conversation):
    conversation.append({"role": "user", "content": message})
    return conversation

def get_message_content(openai_resp):
    return openai_resp.choices[0].message.content

def get_json_resp(openai_resp):
    return json.loads(get_message_content(openai_resp=openai_resp))

def build_website(user_input: UserWebsiteInput, model):
    system_prompt = "You are a helpful assistant which is being used as for generating various elements of website and its content, you will be provided with a json format, each field in the\
json is to be filled properly in accordance with bussiness details given by the user and the description of each and every field described in format"
    website_gen_user_prompt = f"""Here is the json format for the website: 
{website_json_format}
You are free to drop any of the section if you dont think it is usefull in this website and generate content for the sections you will should be there. A website should generally have one of 
products or services section depending on wether the business sells services or products. Here is the bussines description given by user: 
{user_input.to_qna_string()}
Generate the json for the website according to given format"""
    landing_page = None
    if not user_input.landing_page:
        user_prompt = f"Name of the businness: {user_input.name}, Description of bussiness: {user_input.desc}. Output a json having one key 'landing_page' which describes the best suited \
landing page value for given bussiness. Landing page value can be only one of these 6: online_store, professional_service, portfolio, bio_site, landing_page, other"
        landing_page = get_json_resp(call_openai(conversation_history=get_new_conversation(system_prompt=system_prompt, user_prompt=user_prompt), model=model, output_json=True))['landing_page']
    else:
        landing_page = user_input.landing_page

    
    website_data = get_json_resp(call_openai(conversation_history=get_new_conversation(system_prompt=system_prompt, user_prompt=user_input), model=model, output_json=True))
    return landing_page, website_data

def get_next_chat_message(user_message, current_messages=None):
    ai_message = 'Hey'
    website_json = None
    return ai_message, website_json
    

    