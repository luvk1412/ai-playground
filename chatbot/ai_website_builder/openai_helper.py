from openai import OpenAI
from constants import *
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
    website_data = get_json_resp(call_openai(conversation_history=get_new_conversation(system_prompt=system_prompt, user_prompt=website_gen_user_prompt), model=model, output_json=True))
    return landing_page, website_data

def get_next_chat_message(user_message, current_messages, website_data, model):
    new_website_data = None

    is_new_conversation = current_messages is None
    if is_new_conversation:
        system_prompt = f"You are a helpful assistant which is being used in a site builder app, you help user in building a beautiful and informational site for their business, \
give them suggestions to improve certain section's content if asked(one section at a time). Based on this json format: {website_json_format} , \
this is the current website: {website_data}, user can ask you to remove certain sections, add certain sections or modify certains sections in json. \
The changes you can make or only limited to what can be added/removed/modified in json, If user askes to add any new ui component or something like that, \
you should refuse to user in simple language and not mention things like json etc as real user is unaware of that. Your replies should be concise. You should also not call any function in such cases as well"
        current_messages = get_new_conversation(system_prompt=system_prompt, user_prompt=user_message)
    else:
        current_messages = add_user_message(message=user_message, conversation=current_messages)
    response = call_openai(conversation_history=current_messages, functions=functions, model=model)

    if response.choices[0].finish_reason == 'tool_calls':
        current_messages.append(response.choices[0].message)
        tool_call = response.choices[0].message.tool_calls[0]
        argument = json.loads(response.choices[0].message.tool_calls[0].function.arguments)['changes_to_make']

        system_prompt=f"You are a helpful assistant which is being used in a site builder app, you help user in building a beautiful and informational site for their business, \
give them suggestions to improve it and then call appropriate functions to make changes to the website. Based on this json format: {website_json_format} , \
this is the current website: {website_data}, user can ask you to remove certain sections, add certain sections or modify certains sections, and you perform \
those action in accordance with original json fomrat given."
        user_prompt=f"{argument}. Output the modified website json"

        modify_conversation_agent = get_new_conversation(system_prompt=system_prompt, user_prompt=user_prompt)
        new_website_data = get_json_resp(call_openai(conversation_history=modify_conversation_agent, output_json=True, model=model))
        current_messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": f"The website has been modified to {new_website_data}"
            }
        )
        response = call_openai(conversation_history=current_messages, functions=functions, model=model)
        current_messages = add_assistant_message(message=get_message_content(response), conversation=current_messages)
    else:
        current_messages = add_assistant_message(message=get_message_content(response), conversation=current_messages)
    return current_messages, new_website_data