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

def query_channel(twitch_headers):
    URL_GET = requests.get('https://api.twitch.tv/helix/users?login=blondieepanda' , headers=twitch_headers)
    json = URL_GET.json()
    channel_name = json['data'][0]['display_name']
    channel_pfp = json['data'][0]['profile_image_url']
    print(channel_name , channel_pfp)
    return {
        'channel_name' : channel_name,
        'channel_pfp' : channel_pfp
    }

def query_stream(twitch_headers):
    URL_GET = requests.get('https://api.twitch.tv/helix/streams?user_login=blondieepanda' , headers=twitch_headers)
    json = URL_GET.json()
    channel_game_id = json['data'][0]['game_id']
    channel_game = json['data'][0]['game_name']
    print(channel_game_id, channel_game)
    return {
        'channel_game_id' : channel_game_id,
        'channel_game' : channel_game
    }
    
def query_game(twitch_headers , game_id):
    URL_GET = requests.get('https://api.twitch.tv/helix/games?id='+ game_id , headers=twitch_headers,)
    json = URL_GET.json()
    channel_box_art = json['data'][0]['box_art_url']
    print(channel_box_art)
    return {
       'channel_box_art' : channel_box_art
   }

def main():
    twitch_app_token_json = authorize_twitch()
    access_token = twitch_app_token_json['access_token']
    twitch_headers = {
        'Client-ID': os.getenv('twitch_client_id'),
        'Authorization': 'Bearer ' + access_token,
    }
    print('Twitch API Authenticated')

    channel_info = query_channel(twitch_headers) #getting my channel ID and profile picture
    stream_info = query_stream(twitch_headers) #getting my stream information when I go live
    game_info = query_game(twitch_headers , stream_info['channel_game_id']) #getting box art for the game I am currently streaming

    authorize_discord()