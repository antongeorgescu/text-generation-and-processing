import logging
import os
import openai
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')

        prompt = req.params.get('prompt')
        if not prompt:
            try:
                req_body = req.get_body()
                prompt = json.loads(req_body).get('prompt')
            except ValueError:
                pass
        else:
            prompt = req_body.get('prompt')

        if prompt:

            # Load your API key from an environment variable or secret management service
            openai.api_type = "azure"
            openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
            openai.api_version = "2023-09-15-preview"
            openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

            # SYSTEM_ROLE = "Your name is Bobby. You are 12 years old. I need you to write like a 12 year old. Please include misspellings and stereotypical 12 year old boy behaviour including boredom. You are not helpful, you are a 12 year old boy so keep this personna at all times."
            SYSTEM_ROLE = "Your name is Professor Xavier. You are 60 years old. I need to provide me with academic level answers."
            

            message_text = [{"role":"system","content":f"{SYSTEM_ROLE}"},{"role":"user","content":f"{prompt}"}]

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
            logging.info(f'Python HTTP trigger function returned result:{response.choices[0].message.content}')
            return func.HttpResponse(response.choices[0].message.content)
        else:
            logging.error(f"This HTTP triggered function failed due to 'prompt' = {prompt}")
            return func.HttpResponse(
                f"This HTTP triggered function failed due to 'prompt' = {prompt}",
                status_code=422
            )
    except Exception as e:
        logging.error(f"An exception occurred: {e}")
        return func.HttpResponse(f"An exception occurred: {e}",status_code=500)
        
