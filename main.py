import requests
from bs4 import BeautifulSoup
import pandas as pd

def yahoo_financial_statements():

    ticker = input(
        "Input the ticker of the company you'd like to see the financials of: ")

    is_link = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    bs_link = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
    cf_link = f'https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}'

    statements_list = [is_link, bs_link, cf_link]

    headers = []
    temp_list = []
    label_list = []
    final = []
    index = 0

    df_lists = list()

    for link in statements_list:

        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        features = soup.find_all('div', class_='D(tbr)')

        #create headers
        for item in features[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)

        #statement contents
        while index <= len(features)-1:
            #filter for each line of the statement
            temp = features[index].find_all('div', class_='D(tbc)')
            for line in temp:
                #each item added to a temp list
                temp_list.append(line.text)
            #temp_list added to final list
            final.append(temp_list)
            #clear temp_list
            temp_list = []
            index += 1

        df = pd.DataFrame(final[1:])
        df.columns = headers
        # df.index = final[1]

        #function to make all values numerical
        def convert_to_numeric(column):

            first_col = [i.replace(',', '') for i in column]
            second_col = [i.replace('-', '') for i in first_col]
            final_col = pd.to_numeric(second_col)

            return final_col

        for column in headers[1:]:
            df[column] = convert_to_numeric(df[column])

        final_df = df.fillna('-')
        df_lists.append(final_df)

        #reset all lists
        headers = []
        temp_list = []
        label_list = []
        final = []
        index = 0

    return df_lists


for df in yahoo_financial_statements():
    print(df.to_markdown())

# quote = 'TSLA'

# URL = 'https://finance.yahoo.com/quote/' + quote
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.title)
