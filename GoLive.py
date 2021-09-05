import requests
import os

def authorize():
    token_params = {
        'client_id': os.getenv('twitch_client_id'),
        'client_secret': os.getenv('twitch_client_secret'),
        'grant_type': 'client_credentials',
    }

    app_token_request = requests.post(
        'https://id.twitch.tv/oauth2/token', params=token_params)

    return app_token_request.json()

def main():
    twitch_app_token_json = authorize()
    access_token = twitch_app_token_json['access_token']
    twitch_headers = {
        'Client-ID': os.getenv('twitch_client_id'),
        'Authorization': 'Bearer ' + access_token,
    }
    print('Twitch API Authenticated')