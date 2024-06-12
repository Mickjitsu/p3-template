import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
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
    while True:
        print("Please enter your sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break
    
    return sales_data



def validate_data(values):
    """
    This function will convert all string values to integeres
    Raise a valueError if strings cannot be converted into int,
    or if there isn't exactly 6 numbers
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values requires, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True



def update_worksheets(worksheet,data):
    """
    receives worksheet and data info to dynamically update worksheets
    """
    print(f"updating {worksheet} worksheet...")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully")


def calculate_surplus_data(sales_row):
    """
    compare sales with stock and surplus for each item type
    """
    print("Calculating surplus data..\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    returns the last 5 row rentries for each sandwich on sales worksheet
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    program to calculate average of stock data
    """
    print("calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data



def main():
    """
    run all program functions
    """
    
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheets("sales", sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheets("surplus", new_surplus_data)
    get_last_5_entries_sales()
    sales_columns = get_last_5_entries_sales()
    calculate_stock_data(sales_columns)
    stock_data = calculate_stock_data(sales_columns)
    update_worksheets("stock", stock_data)
    print(stock_data)


print("Welcome to love sandwiches data automation")

main()

