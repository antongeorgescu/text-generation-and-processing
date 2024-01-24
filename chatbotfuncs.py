# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(chatbotfuncs) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
import openai
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

app = func.Blueprint()

@app.route(route="greeting",auth_level=func.AuthLevel.FUNCTION)
def greeting(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="textSummary", auth_level=func.AuthLevel.FUNCTION)
def textSummary(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
    else:
        text = req_body.get('text')

    if text:
        # Load your API key from an environment variable or secret management service
        openai.api_type = "azure"
        openai.api_base = "https://openai-arch-v.openai.azure.com/"
        openai.api_version = "2023-09-15-preview"
        openai.api_key = 'fd2e0aa746cf48efa326e6c360915d88' #os.getenv("OPENAI_API_KEY")

        SYSTEM_ROLE = "You are an AI assistant that helps people find information."
        USER_PROMPT = "Provide a summary of the text below that captures its main idea."

        message_text = [{"role":"system","content":f"{SYSTEM_ROLE}"},{"role":"user","content":f"{USER_PROMPT}\\n\\n{text}"}]

        # Make a request to the API
        response = openai.ChatCompletion.create(
            engine="slp-chatbot-text-summary",
            messages = message_text,
            temperature=0.7,
            max_tokens=500,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        
        return func.HttpResponse(response.choices[0].message.content)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="listResourceGroup", auth_level=func.AuthLevel.FUNCTION)
def listResourceGroup(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rgname = req.params.get('name')
    if not rgname:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            rgname = req_body.get('resgrp')

    if rgname:
        credential = DefaultAzureCredential()
        subscription_id = 'bfb59099-69db-4d2b-887e-abcf6ccdb5c4'
        resource_client = ResourceManagementClient(credential, subscription_id)

        resource_group_name = rgname

        resource_list = resource_client.resources.list_by_resource_group(resource_group_name)

        listOut = f"Resource Group {rgname} contains:"
        for resource in resource_list:
            listOut = f"{listOut},{resource.name}"
        return func.HttpResponse(f"{listOut}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )