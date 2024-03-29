import logging
import os
import openai
import json

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')

        text = req.params.get('text')
        if not text:
            try:
                body_bytes = req.get_body()
                body_json = body_bytes.decode('utf8').replace("\\'",'\\').replace("\\","").replace('"{','{').replace('}"','}')
                # logging.info(f"Body bytes:{body_json}")
                
                text = json.loads(body_json).get("text")
                logging.info(f"Body text:{text}")
            except ValueError:
                pass
        else:
            text = req.get_body().get('text')

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
            logging.info(f"This HTTP triggered function returned result {response.choices[0].message.content}")
            summary = '{"summary":"' + response.choices[0].message.content + '"}'
            return func.HttpResponse(summary,status_code=200)
        
        else:
            logging.error(f"This HTTP triggered function failed due to 'text' = {text}")
            return func.HttpResponse(
                '{"error" :' + f"This HTTP triggered function failed due to 'text' = {text}" + '"}',
                status_code=422
            )
    except Exception as e:
        logging.error(f"An exception occurred: {e}")
        return func.HttpResponse('{"error" :' + f"An exception occurred: {e}"+ '"}',status_code=500)
        