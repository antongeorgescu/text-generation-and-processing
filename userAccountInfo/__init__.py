import logging
import json
import azure.functions as func

users = '[{"sin":"123456789","name":"Johnny Cecotto","address":"1234 Victoria Blvd, Victoria, BC","province":"British Columbia"},{"sin":"112233445","name":"Tonino Alvianda","address":"453 Upper Middle Rd, Fredericton, NB","province":"New Brunswick"},{"sin":"122334456","name":"Jannick Sinner","address":"765 Bristol Circle, Mississauga, ON","province":"Ontario"},{"sin":"987654321","name":"Bing Nadalargaard","address":"3452 Quuensway Blvd, North Bay, ON","province":"Ontario"}]'

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    sinid = req.params.get('sin')
    if not sinid:
        try:
            req_body = req.get_json()
            sinid = req_body.get('sin')
        except ValueError:
            pass
        else:
            sinid = req_body.get('sin')

    if sinid:
        # Load the JSON array into a Python list
        userdata = json.loads(users)
        # Define the attribute and value you're looking for
        attribute, value = "sin", sinid

        # Check if an item with the specified attribute value exists
        user = next((item for item in userdata if item.get(attribute) == value),None)
        if user:
            # return func.HttpResponse('{"name":"' + {user["name"]} + '","address":"' + {user["address"]} + '","province":"' + {user["province"]} + '"}')  
            return func.HttpResponse(json.dumps(user))  
        else: 
            logging.info(f"No user found with sin:{sinid}.")
            return func.HttpResponse(f"No user found with sin:{sinid}.")
    else:
        logging.error('This HTTP triggered function failed to execute as no sin# parameter has been passed.')
        return func.HttpResponse(
             "This HTTP triggered function failed to execute as no sin# parameter has been passed.",
             status_code=422
        )
