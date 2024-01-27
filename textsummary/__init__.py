import logging
import os
import openai

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get('text')
        except ValueError:
            pass
    else:
        text = req_body.get('text')

    if text:
        # Load your API key from an environment variable or secret management service
        openai.api_type = "azure"
        openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
        openai.api_version = "2023-09-15-preview"
        openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

        SYSTEM_ROLE = "You are an AI assistant that helps people find information."
        USER_PROMPT = "Provide a summary of the text below that captures its main idea."

        message_text = [{"role":"system","content":f"{SYSTEM_ROLE}"},{"role":"user","content":f"{USER_PROMPT}\\n\\n{text}"}]

        # Make a request to the API
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), 
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
