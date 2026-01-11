from weeb_cli.services.api import api_client

def search(query):
    return api_client.search(query)
