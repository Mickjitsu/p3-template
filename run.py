import gspread
from google.oauth2.service_account import Credentials
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('cred.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches_proj')

def get_sales_data():
    """
    Get Sales figures input from user
    """
    print("Please enter your sales data from the last market.")
    print("Data should be six numbers, seperated by commas.")
    print("Example: 10,20,30,40,50,60")

    data_str = input("Enter your data here: ")
    
    sales_data = data_str.split(",")
    print(sales_data)
    validate_data(sales_data)


def validate_data(values):
    """
    This function will convert all string values to integeres
    Raise a valueError if strings cannot be converted into int,
    or if there isn't exactly 6 numbers
    """
    print(values)
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values requires, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")

get_sales_data()