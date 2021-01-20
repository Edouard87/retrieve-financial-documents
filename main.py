import requests
from bs4 import BeautifulSoup
import pandas as pd

def yahoo_financial_statements():

    # Get User Data
    ticker = input("Input the ticker of the company you'd like to see the financials of: ")

    # Get links
    is_link = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    bs_link = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
    cf_link = f'https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}'

    # Create list (for while loop below)
    statements_list = [is_link, bs_link, cf_link]

    # Init variables for later
    headers = []
    temp_list = []
    label_list = []
    final = []
    index = 0
    df_lists = list()

    # For each link in the statements list, create a new pandas data frame
    for link in statements_list:

        # Get page and input into BeautifulSoup
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        # 
        features = soup.find_all('div', class_='D(tbr)')

        # Get Headers
        for item in features[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)
        
        while index <= len(features)-1:
            temp = features[index].find_all('div', class_='D(tbc)')
            for line in temp:
                temp_list.append(line.text)
            final.append(temp_list)
            temp_list = []
            index += 1

        # Create the data frame
        df = pd.DataFrame(final[1:])
        df.columns = headers

        # Make data in data frame numeric
        def convert_to_numeric(column):

            first_col = [i.replace(',', '') for i in column]
            second_col = [i.replace('-', '') for i in first_col]
            final_col = pd.to_numeric(second_col)

            return final_col

        for column in headers[1:]:
            df[column] = convert_to_numeric(df[column])

        final_df = df.fillna('-')
        df_lists.append(final_df)

        # Reset all lists
        headers = []
        temp_list = []
        label_list = []
        final = []
        index = 0
        
    # Return a list of df lists
    return df_lists

# Print each table

statements = yahoo_financial_statements()
for i in range(0,len(statements)):
    df = statements[i]
    print("# Table " + str(i + 1))
    print(df.to_markdown())
