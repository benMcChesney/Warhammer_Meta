
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
    parser.add_argument('--entity', type=str, help='API object')

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

    if args.entity:
        print(f"entity: {args.entity}")
        if ( args.entity == 'events'):
                getEvents( args )
        else:
            print('other entity' + entity )
    else:
        args.entity = datetime.now().date().strftime('%Y-%m-%d')
        print(f"No entity provided, exiting")
        exit(-1)
    print('end of run')

def getEvents( args ):

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Access data from the INI file
    client_id = config['bcp']['client_id']
    limit = 100 

    # Define the URL you want to send the GET request to
    #url = 'https://newprod-api.bestcoastpairings.com/v1/events?limit=40&startDate=2024-08-28T07%3A00%3A00Z&endDate=2024-10-31T07%3A00%3A00Z&sortKey=eventDate&sortAscending=true&sortAsc=true&sortType=Start+Date+Ascending&gameType=4'
    
    url = f'https://newprod-api.bestcoastpairings.com/v1/{args.entity}?limit={limit}&sortAscending=true&sortKey=eventDate&startDate={args.startDate}&endDate={args.endDate}&gameType=4'

    print( url )         

    #             
    # Set up the headers with the bearer token
    headers = {
        'client-id':client_id
         , 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)'

    }


    # start Loop - go until results < max 
    bContinue = True 
    df_append = pd.DataFrame({})
    lastEventDate = args.startDate
    pageIndex = 0 

    while bContinue == True :
        
        url = f'https://newprod-api.bestcoastpairings.com/v1/{args.entity}?limit={limit}&sortAscending=true&sortKey=eventDate&startDate={lastEventDate}&endDate={args.endDate}&gameType=4'
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print('Success!')
            # Normalize the nested JSON data
            df = json_normalize( response.json()["data"] )

            expanded_placing_df = json_normalize(df['placingMetrics'])
            
            # Combine the expanded DataFrame with the original DataFrame
            df_data = df.drop(columns=['placingMetrics']).join(expanded_placing_df)

            df_append = pd.concat([df_append, df_data], ignore_index=True)
           
            #df_playerMetrics = json_normalize( df_data )
            #df_data = df.drop(columns=['playerPlacingMetrics']).join(df_playerMetrics)
            lastEventDate = df_data['eventDate'].max()
            print(f'appended, @ [{pageIndex}] now + {len(df_data)} - new total {len(df_append)} last date - {lastEventDate}')
            pageIndex = pageIndex + 1 
            if ( len(df_data) < 100 ):
                bContinue = False 
                print('end of loop!')
        else:
            print(f'Failed to retrieve data: {response.status_code}')
    
    df_append.to_csv( 'data/test.csv')

    
if __name__ == '__main__':
    main()
