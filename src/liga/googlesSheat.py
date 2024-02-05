from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pprint import pprint
from googleapiclient import discovery
from dotenv import load_dotenv
import os
import requests


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    load_dotenv()

    api_key = os.getenv('STEAM_API_KEY')

    steamApiKey = api_key
    steamID = "76561198094261580"
    gameID = ""
    

    #Steam API link formatting for "GetOwnedGames"
    glink1 = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
    glink2 = "&steamid=" + steamID + "&include_appinfo=1&format=json"
    glink = glink1 + steamApiKey + glink2

    alink1 = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid="
    alink2 = "&steamid=" + steamID + "&l=spanish&include_appinfo=1&format=json"

    #Sent API Get request and save respond to a variable
    r = requests.get(glink)
    
    #convert to JSON and save to another variable
    steam = r.json()


    #JSON output with information about each game owned
    #print(steam)
    #https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_.28v0001.29
    
    #Getting integer value of total games owned
    totalGames = str(steam["response"]["game_count"])
    
    #Output total games owned
    #print(totalGames)
    #Some logic for getting a random game from account with over 10 hours playtime
    steamGame = ""
    steamGames = []
    headers = ["Game", "Playtime", 'TotalAchievements', 'Achieved']

    for item in steam["response"]["games"]:
        body = []
        steamGame = item["name"]
        gameID = item['appid']
        alink = alink1 + str(gameID) + "&key=" + steamApiKey + alink2
        a = requests.get(alink)
        achievements = a.json()
        comp = 0
        total = 0
        try:
            for achievement in achievements['playerstats']['achievements']:
                total= total + 1
                if achievement['achieved'] == 1:
                    comp= comp + 1
                body.append([steamGame, achievement['name'], achievement['description'] ,bool(achievement['achieved'])])
        except :
            pass
        try:
            service = discovery.build('sheets', 'v4', credentials=creds)

            # The ID of the spreadsheet to update.
            spreadsheet_id = '17t3E8FqYa0kZ8Src-yiBJKPI1JArcYgp6Oe1Da5Ekoc'  # TODO: Update placeholder value.

            # The A1 notation of a range to search for a logical table of data.
            # Values will be appended after the last row of the table.
            range_ = "A:A"  # Update placeholder value.

            # How the input data should be interpreted.
            value_input_option = 'RAW'  # TODO: Update placeholder value.

            # How the input data should be inserted.
            insert_data_option = 'OVERWRITE'  # TODO: Update placeholder value.

            value_range_body = {
                
                "range": "A:A",
                "values": body,
                "majorDimension": "ROWS"
            }
            print(value_range_body)
            request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
            response = request.execute()

            # TODO: Change code below to process the `response` dict:
            pprint(response)
        except HttpError as err:
            print(err)


if __name__ == '__main__':
    main()