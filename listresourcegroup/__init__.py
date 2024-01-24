import os
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rgname = req.params.get('resgrp')
    if not rgname:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            rgname = req_body.get('resgrp')

    if rgname:
        credential = DefaultAzureCredential()
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
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
