import requests
import os

def authorize():
    token_params = {
        'client_id': os.getenv('twitch_client_id'),
        'client_secret': os.getenv('twitch_client_secret'),
        'grant_type': 'client_credentials',
    }

    print(token_params['client_id'])
    app_token_request = requests.post(
        'https://id.twitch.tv/oauth2/token', params=token_params)
    print(app_token_request.content)

    return app_token_request.json()

def main():
    twitch_app_token_json = authorize()
    access_token = twitch_app_token_json['access_token']
    print('access token: ' + access_token)
    twitch_headers = {
        'Client-ID': os.getenv('twitch_client_id'),
        'Authorization': 'Bearer ' + access_token,
    }
    requests.get('https://id.twitch.tv/oauth2/validate',
                 headers=twitch_headers)