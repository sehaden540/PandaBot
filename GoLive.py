import requests
import os
import discord

discord_client = discord.Client()

def authorize_discord():
    TOKEN = os.getenv('discord_token')
    discord_client.run(TOKEN)

@discord_client.event
async def on_ready():
    print(f'{discord_client.user} has connected to Discord!')
    await discord_client.close()

def authorize_twitch():
    token_params = {
        'client_id': os.getenv('twitch_client_id'),
        'client_secret': os.getenv('twitch_client_secret'),
        'grant_type': 'client_credentials',
    }

    app_token_request = requests.post(
        'https://id.twitch.tv/oauth2/token', params=token_params)

    return app_token_request.json()

def main():
    twitch_app_token_json = authorize_twitch()
    access_token = twitch_app_token_json['access_token']
    twitch_headers = {
        'Client-ID': os.getenv('twitch_client_id'),
        'Authorization': 'Bearer ' + access_token,
    }
    print('Twitch API Authenticated')

    authorize_discord()