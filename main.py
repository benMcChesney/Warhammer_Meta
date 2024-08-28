
import argparse
from datetime import datetime



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

if __name__ == '__main__':
    main()
