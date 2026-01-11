from weeb_cli.services.api import api_client

def get_streams(slug, episode):
    return api_client.get_streams(slug, episode)
