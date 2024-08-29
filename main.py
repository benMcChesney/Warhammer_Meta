
import argparse
from datetime import datetime
import requests
from pathlib import Path
import configparser
import pandas as pd
import pandas as pd
import pandas as pd
from pandas import json_normalize



def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='BCP API retrieve data')

    # Add arguments
    parser.add_argument('--startDate', type=str, help='start date of search ')
    parser.add_argument('--endDate', type=str, help='end date of search')

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.startDate:
        print(f"startDate: {args.startDate}")
    else:
        print("No start date provided ERROR.")

    if args.endDate:
        print(f"endDate: {args.endDate}")
    else:
        
        args.endDate = datetime.now().date().strftime('%Y-%m-%d')
        print(f"No end date provided defaulting to today endDate: {args.endDate}")

    getEvents( args )



def getEvents( args ):

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Access data from the INI file
    client_id = config['bcp']['client_id']

    # Define the URL you want to send the GET request to
    #url = 'https://newprod-api.bestcoastpairings.com/v1/events?limit=40&startDate=2024-08-28T07%3A00%3A00Z&endDate=2024-10-31T07%3A00%3A00Z&sortKey=eventDate&sortAscending=true&sortAsc=true&sortType=Start+Date+Ascending&gameType=4'
    
    url = f'https://newprod-api.bestcoastpairings.com/v1/events?limit=100&sortAscending=true&sortKey=eventDate&startDate={args.startDate}&endDate={args.endDate}&gameType=4'

    print( url )         

    #          , 'Authorization': f'Bearer {bearer_token}'      
    # Set up the headers with the bearer token
    headers = {
        'client-id':client_id
         , 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)'
    }

    # Send the GET request with bearer token authentication
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print('Success!')
        #print(response.json())  # Assuming the res ponse is JSON data
        # Normalize the nested JSON data
        df = json_normalize( response.json()["data"] )
        print ( df.head(5) )
        df.to_csv( 'test.csv')
    else:
        print(f'Failed to retrieve data: {response.status_code}')

    print('end of run')
if __name__ == '__main__':
    main()
