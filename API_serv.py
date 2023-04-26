# Use NHL API service to collect and update information about Players, Teams, Games, etc.
from cmd import IDENTCHARS
import json
from urllib import response
import requests
from Constants import *
from functools import reduce
import operator
#########################################################################################
# http get to retrieve NHL API JSON


def http_get(endpoint):
    api_response = requests.get(
        BASE_URL+endpoint, params={"Content-Type": "application/json"})
    return api_response.json()

#########################################################################################
# Services for Player class
##


def get_player(player_id):
    api_response = http_get(ENDPOINT_DICT['get_player'].format(player_id))
    return api_response['people']


def get_game_log(player_id):
    api_response = http_get(
        ENDPOINT_DICT['get_game_log'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def season_stat(player_id):
    api_response = http_get(
        ENDPOINT_DICT['season_stat'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def div_split(player_id):
    api_response = http_get(
        ENDPOINT_DICT['div_split'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def mon_split(player_id):
    api_response = http_get(
        ENDPOINT_DICT['mon_split'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def week_split(player_id):
    api_response = http_get(
        ENDPOINT_DICT['week_split'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def league_stat(player_id):
    api_response = http_get(
        ENDPOINT_DICT['league_stat'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def season_pace(player_id):
    # only works in season per API
    api_response = http_get(
        ENDPOINT_DICT['season_pace'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def sit_goals(player_id):
    api_response = http_get(
        ENDPOINT_DICT['sit_goals'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def day_split(player_id):
    api_response = http_get(
        ENDPOINT_DICT['day_split'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def home_away_split(player_id):
    api_response = http_get(
        ENDPOINT_DICT['home_away_split'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def win_loss_split(player_id):
    api_response = http_get(
        ENDPOINT_DICT['win_loss_split'].format(player_id, CURRENT_SEASON))
    return api_response['stats'][0]['splits']


def player_schedule(id):
    pass
    # needs to look up the player's team and then pull the teams schedule for the player


# Services for Game class
##

def game_box(game_id):
    api_response = http_get(ENDPOINT_DICT['game_box'].format(game_id))
    return api_response['teams']


def game_live(game_id):
    api_response = http_get(ENDPOINT_DICT['game_live'].format(game_id))
    return api_response['liveData']['plays']


# Services for Team class
##


# get all teams
def fetch_teams():
    api_response = http_get(ENDPOINT_DICT['fetch_teams'])
    return api_response['teams']


def team_schedule(team_id):
    api_response = http_get(ENDPOINT_DICT['team_schedule'].format(
        team_id, START_DATE, END_DATE))
    return api_response


def team_roster(team_id):
    api_response = http_get(ENDPOINT_DICT['team_roster'].format(team_id))
    return api_response['teams'][0]['roster']['roster']
