import logging
import json
from dotenv import load_dotenv, find_dotenv
import requests
import time
import os
import re

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

logging.basicConfig(
    filename='./name_banned.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    return {
        'URLS_RCON': os.environ['URLS_RCON'].split(','),
        'URL_LOGIN': os.environ['URL_LOGIN'],
        'URL_GET_PLAYERS': os.environ['URL_GET_PLAYERS'],
        'USER_RCON': os.environ['USER_RCON'],
        'PASSWORD_RCON': os.environ['PASSWORD_RCON'],
        'MSG_WARNING': os.environ['MSG_WARNING'],
        'URL_MESSAGE': os.environ['URL_MESSAGE'],
        'URL_POST_PLAYER_COMMENT': os.environ['URL_POST_PLAYER_COMMENT'],
        'URL_ADD_BLACKLIST': os.environ['URL_ADD_BLACKLIST'],
        'ERROR_LOGIN_MSG': os.environ['ERROR_LOGIN_MSG'],
        'ERROR_IN_MSG': os.environ['ERROR_IN_MSG'],
        'MSG_TO_MSG': os.environ['MSG_TO_MSG'],
        'UNEXPECTED_ERROR_MSG': os.environ['UNEXPECTED_ERROR_MSG'],
        "BAN_MSG": os.environ['BAN_MSG'],
        "NUM_WARNINGS": int(os.environ['NUM_WARNINGS']),
        "ENABLE_BAN": os.environ['ENABLE_BAN'].lower() == "true",
        "SUCCESSFUL_BAN_MSG": os.environ['SUCCESSFUL_BAN_MSG'],
        "REASON_MSG": os.environ['REASON_MSG'],
        "DISCORD_WEBHOOK_URL": os.environ['DISCORD_WEBHOOK_URL'],
        "DISCORD_MSG": os.environ['DISCORD_MSG'],
        "REGEX": os.environ['REGEX']
    }

config = load_config()

players_warning_list = []

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

def send_msg(session, data, url_rcon):
    json_data = {
        'comment': '',
        'duration_hours': 2,
        'message': f'{config["MSG_WARNING"]}',
        'player_id': f'{data["player_id"]}',
        'player_name': f'{data["player_name"]} -',
        'reason': config['MSG_WARNING'],
        'save_message': True
    }
    try:
        response = session.post(f'{url_rcon}{config["URL_MESSAGE"]}', json=json_data)
        response.raise_for_status()
        logging.info(f'{config["MSG_TO_MSG"]} {data["player_name"]} - {data["player_id"]}')
        if(config['ENABLE_BAN'] == True):
            set_player_warning(session, url_rcon, data)
    except requests.exceptions.RequestException as e:
        logging.error(f'{config["ERROR_IN_MSG"]} {url_rcon}{config["URL_MESSAGE"]}: {e}')

def filter_name(session, player_list, url_rcon):
    id_list = []
    for player in player_list:
        name = player['name']
        if not re.search(config['REGEX'], name):
            logging.info(f'{player["player_id"]}, {name}')
            id_list.append({'player_name': name, 'player_id': player['player_id']})
    for obj in id_list:
        send_msg(session, obj, url_rcon)
        
def set_player_warning(session, url_rcon, data):
    global players_warning_list
    if(len(players_warning_list) > 0):
        for player in players_warning_list:
            if any(player.values()) and player['player_id'] == data['player_id']:
                if(player['num_warnings'] <= int(config['NUM_WARNINGS'])):
                    player['num_warnings'] = player['num_warnings'] + 1
                else:
                    permaban_player(session, url_rcon, data)
                    players_warning_list = [player for player in players_warning_list if player['player_id'] != data['player_id']]
            else:
                players_warning_list.append(create_player_warning(data))
    else:
        if(int(config['NUM_WARNINGS']) == 0):            
            logging.info(f'{data} perma')
            permaban_player(session, url_rcon, data)
        else:
            players_warning_list.append(create_player_warning(data))

def create_player_warning(data):
    return {"player_id": data['player_id'],"player_name": data['player_name'],"num_warnings": 1}

def permaban_player(session, url_rcon, data): 
    post_msg_json = {
        "comment": f'Player ID {data["player_id"]} perma banned for wrong name',
        "player_id": data['player_id']
    }
    try:
        response_first_msg = session.post(f'{url_rcon}{config["URL_POST_PLAYER_COMMENT"]}', json=post_msg_json)
        response_first_msg.raise_for_status()
        if(json.loads(response_first_msg.text).get('failed', []) == False):
            try:
                response_add_blacklist = session.post(f'{url_rcon}{config["URL_ADD_BLACKLIST"]}', json={"blacklist_id": 0, "expires_at": "3000-02-19T22:24:00.000Z", "player_id": str(data["player_id"]), "reason": config['BAN_MSG']})
                response_add_blacklist.raise_for_status()
                if(json.loads(response_add_blacklist.text).get('failed', []) == False):
                    if(config['DISCORD_WEBHOOK_URL']):
                        send_discord_message(data)
                    logging.info(f'{config["SUCCESSFUL_BAN_MSG"]} {data["player_name"]} - {data["player_id"]}')
                        
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                logging.error(f'{config["ERROR_IN_MSG"]} {url_rcon}{config["URL_ADD_BLACKLIST"]}: {e}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logging.error(f'{config["ERROR_IN_MSG"]} {url_rcon}{config["URL_POST_PLAYER_COMMENT"]}: {e}')

def send_discord_message(data):
    try:
        webhook_url = config['DISCORD_WEBHOOK_URL']
        data = {
            "content": config["DISCORD_MSG"],
        }
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f'Error al enviar el mensaje a Discord: {e}')
    
def init_process():
    while True:
        try:
            with requests.Session() as session:
                for url_rcon in config["URLS_RCON"]:
                    try:
                        if login(session, url_rcon) != False:
                            players = get_players(session, url_rcon)
                            if players:
                                filter_name(session, players, url_rcon)
                    except Exception as e:
                        logging.error(f"{config['UNEXPECTED_ERROR_MSG']}: {e}")
        except Exception as e:
            logging.error(f"{config['UNEXPECTED_ERROR_MSG']}: {e}")
        finally:
            time.sleep(10*60)
    

init_process()
