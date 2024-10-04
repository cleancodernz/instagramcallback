import azure.functions as func
import logging
import requests
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)



def exchange_auth_code(auth_code):
    url = 'https://api.instagram.com/oauth/access_token'
    payload = {
        'client_id': '<YOUR_CLIENT_ID>',
        'client_secret': '<YOUR_CLIENT_SECRET>',
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://<your-storage-account-name>.z13.web.core.windows.net/oauth/callback.html',
        'code': auth_code
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json()  # This contains the access token
    else:
        return None


@app.route(route="instagramcallback")
def instagramcallback(req: func.HttpRequest) -> func.HttpResponse:
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