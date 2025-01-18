import logging
import json
from dotenv import load_dotenv, find_dotenv
import requests
import os
import re

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

logging.basicConfig(
    filename='./name_banned.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

config = {
    'URLS_RCON': os.environ['URLS_RCON'].split(','),
    'URL_LOGIN': os.environ['URL_LOGIN'],
    'URL_GET_PLAYERS': os.environ['URL_GET_PLAYERS'],
    'USER_RCON': os.environ['USER_RCON'],
    'PASSWORD_RCON': os.environ['PASSWORD_RCON'],
    'MSG_WARNING': os.environ['MSG_WARNING'],
    'URL_MESSAGE': os.environ['URL_MESSAGE'],
    'ERROR_LOGIN_MSG': os.environ['ERROR_LOGIN_MSG'],
    'ERROR_IN_MSG': os.environ['ERROR_IN_MSG'],
    'MSG_TO_MSG': os.environ['MSG_TO_MSG'],
    'UNEXPECTED_ERROR_MSG': os.environ['UNEXPECTED_ERROR_MSG']
}

def login(session, url_rcon):
    try:
        response = session.post(f'{url_rcon}{config["URL_LOGIN"]}', json={'username': config["USER_RCON"], 'password': config["PASSWORD_RCON"]})
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f'{config["ERROR_LOGIN_MSG"]} {url_rcon}{config["URL_LOGIN"]}: {e}')
        return False

def get_players(session, url_rcon):
    try:
        response = session.get(f'{url_rcon}{config["URL_GET_PLAYERS"]}')
        response.raise_for_status()
        return json.loads(response.text).get('result', [])
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logging.error(f'{config["ERROR_IN_MSG"]} {url_rcon}{config["URL_GET_PLAYERS"]}: {e}')
        return []

def send_msg(session, data, url_rcon):
    json_data = {
        'comment': '',
        'duration_hours': 2,
        'message': config['MSG_WARNING'],
        'player_id': f'{data["id"]}',
        'player_name': f'{data["name"]} -',
        'reason': config['MSG_WARNING'],
        'save_message': True
    }
    try:
        response = session.post(f'{url_rcon}{config["URL_MESSAGE"]}', json=json_data)
        response.raise_for_status()
        logging.info(f'{config["MSG_TO_MSG"]} {data["name"]} - {data["id"]}')
    except requests.exceptions.RequestException as e:
        logging.error(f'{config["ERROR_IN_MSG"]} {url_rcon}{config["URL_MESSAGE"]}: {e}')

def filter_name(session, player_list, url_rcon):
    regex = r".*[A-Za-z0-9.]{3}.*"
    id_list = []
    for player in player_list:
        name = player['name']
        if not re.search(regex, name):
            id_list.append({'name': player['name'], 'id': player['player_id']})
    for obj in id_list:
        send_msg(session, obj, url_rcon)

def init_process():    
    with requests.Session() as session:
        for url_rcon in config["URLS_RCON"]:
            try:
                if login(session, url_rcon) != False:
                    players = get_players(session, url_rcon)
                    if players:
                        filter_name(session, players, url_rcon)
            except requests.exceptions.RequestException as e:
                logging.error(f"{config['UNEXPECTED_ERROR_MSG']}: {e}")

init_process()