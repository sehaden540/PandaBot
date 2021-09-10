import requests
import os
import discord
import re

discord_client = discord.Client()
channel_info = {}
stream_info = {}
game_info = {}


def authorize_discord():
    TOKEN = os.getenv('discord_token')
    discord_client.run(TOKEN)


def create_message(channel_info, stream_info, game_info):
    embed = discord.Embed(title=stream_info['stream_title'], url=os.getenv(
        'stream_link'), color=0x6a00ff)
    embed.set_author(
        name=channel_info['channel_name'], icon_url=channel_info['channel_pfp'])
    embed.set_thumbnail(url=game_info['channel_box_art'])
    embed.add_field(
        name='Game', value=stream_info['channel_game'], inline=False)
    embed.set_image(url=stream_info['thumbnail_url'])
    return embed


async def send_message(embed):
    channel_id = os.getenv('discord_channel_id')
    channel = discord_client.get_channel(int(channel_id))
    await channel.send(embed=embed)


@discord_client.event
async def on_ready():
    embed = create_message(channel_info, stream_info, game_info)
    await send_message(embed)
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
    URL_GET = requests.get(
        'https://api.twitch.tv/helix/users?login=blondieepanda', headers=twitch_headers)
    json = URL_GET.json()
    channel_name = json['data'][0]['display_name']
    channel_pfp = json['data'][0]['profile_image_url']
    return {
        'channel_name': channel_name,
        'channel_pfp': channel_pfp
    }


def query_stream(twitch_headers):
    URL_GET = requests.get(
        'https://api.twitch.tv/helix/streams?user_login=blondieepanda', headers=twitch_headers)
    json = URL_GET.json()
    stream_title = json['data'][0]['title']
    channel_game_id = json['data'][0]['game_id']
    channel_game = json['data'][0]['game_name']
    thumbnail_url = json['data'][0]['thumbnail_url']
    thumbnail_url = re.sub('\{.*\}', '1920x1080', thumbnail_url)
    return {
        'stream_title': stream_title,
        'channel_game_id': channel_game_id,
        'channel_game': channel_game,
        'thumbnail_url': thumbnail_url
    }


def query_game(twitch_headers, game_id):
    URL_GET = requests.get(
        'https://api.twitch.tv/helix/games?id=' + game_id, headers=twitch_headers,)
    json = URL_GET.json()
    channel_box_art = json['data'][0]['box_art_url']
    channel_box_art = re.sub('\{.*\}', '200x300', channel_box_art)
    return {
        'channel_box_art': channel_box_art
    }


def main():
    twitch_app_token_json = authorize_twitch()
    access_token = twitch_app_token_json['access_token']
    twitch_headers = {
        'Client-ID': os.getenv('twitch_client_id'),
        'Authorization': 'Bearer ' + access_token,
    }

    # getting my channel ID and profile picture
    global channel_info
    channel_info = query_channel(twitch_headers)
    # getting my stream information when I go live
    global stream_info
    stream_info = query_stream(twitch_headers)
    # getting box art for the game I am currently streaming
    global game_info
    game_info = query_game(twitch_headers, stream_info['channel_game_id'])

    authorize_discord()
