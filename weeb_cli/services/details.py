from weeb_cli.services.api import api_client

def get_details(slug):
    return api_client.get_details(slug)
