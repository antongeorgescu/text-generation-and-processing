import logging
import json
# import ssl
import azure.functions as func
import certifi
certifi.where()

import warnings
warnings.filterwarnings("ignore")

import openai
import time
import pkg_resources

openai.api_key = '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'
assistant_id = 'asst_OgDM2DxsDQbQn7Wd2bUAslhz'

def create_thread(ass_id,prompt):
    #Get Assitant
    #assistant = openai.beta.assistants.retrieve(ass_id)

    #create a thread
    thread = openai.threads.create()
    my_thread_id = thread.id


    #create a message
    message = openai.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )

    #run
    run = openai.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=ass_id,
    ) 

    return run.id, thread.id


def check_status(run_id,thread_id):
    run = openai.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')

        # Replace 'package_name' with the name of your package
        package_name = 'openai'
        package_version = pkg_resources.get_distribution(package_name).version

        logging.info(f"{package_name} version is {package_version}")

        prompt = req.params.get('prompt')
        if not prompt:
            try:
                body_bytes = req.get_body()
                body_json = body_bytes.decode('utf8').replace("\\'",'\\').replace("\\","").replace('"{','{').replace('}"','}')
                # logging.info(f"Body bytes:{body_json}")
                
                prompt = json.loads(body_json).get("prompt")
                logging.info(f"Body content:{prompt}")
            except ValueError:
                pass
        else:
            prompt = req.get_body().get('prompt')

        if prompt:
            my_run_id, my_thread_id = create_thread(assistant_id,f"[topic]: {prompt}")
            status = check_status(my_run_id,my_thread_id)
            while (status != "completed"):
                status = check_status(my_run_id,my_thread_id)
                time.sleep(2)
            response = openai.beta.threads.messages.list(
            thread_id=my_thread_id
            )

            if response.data:
                logging.info(f"This HTTP triggered function returned result {response.data[0].content[0].text.value}")
                summary = '{"answer":"' + response.data[0].content[0].text.value + '"}'
                return func.HttpResponse(summary,status_code=200)
        else:
            logging.error(f"This HTTP triggered function failed due to 'text' = {prompt}")
            return func.HttpResponse(
                '{"error" :' + f"This HTTP triggered function failed due to 'text' = {prompt}" + '"}',
                status_code=422
            )
    except Exception as e:
        logging.error(f"An exception occurred: {e}")
        return func.HttpResponse('{"error" :' + f"An exception occurred: {e}"+ '"}',status_code=500)