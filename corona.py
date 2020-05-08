import requests
import urllib.request
from urllib.request import Request, urlopen
import time
from time import sleep
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt

provinces = ["Ontario", "British Columbia", "Canada", "Quebec", "Alberta", "Repatriated Travellers", "Saskatchewan",
             "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Prince Edward Island", "Nova Scotia",
             "Northwest Territories", "Nunavut", "Yukon"]

def covid_summary():
    # the target we want to open
    url = 'https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html'
    response = requests.get(url)

    # http_respone 200 means OK status
    if response.status_code == 200:
        ##make it open the page
        page = urllib.request.urlopen(url)

        ##processing the req as browser agent
        req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(webpage, 'html.parser')

        ##scraping the total covid tested count
        total_tested = soup.find_all('div', attrs={'class': 'col-md-4'})

        ##scraping the time
        as_of_time = soup.find_all('div', attrs={'class': 'col-md-7'})

        ##stripping xml tags
        result2 = re.search('<p class="text-right h3 mrgn-tp-sm">(.*)</p>', str(as_of_time[0]))
        result = re.search('<p class="h2 mrgn-tp-md">(.*)</p>', str(total_tested[1]))

        ##print the result from the re.search
        print("As of: ", result2.group(1))
        print("In Canada, the following number of people have been tested:", result.group(1))


    else:
        print("Error")


def covid_pr(province, nodays):
    data = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv')
    #print(transactions.columns.tolist())
    ##print(data[['prname', 'numtoday', 'percentoday']])

    data.rename(columns={'prname': 'Province', "numtotal": "Total Positive", "numtoday": "Today Positive",
                         "numtested": "Total Tested", "percentoday": "% Increase"}, inplace=True)

    ##filter out provincial data
    df1 = data[data['Province'].str.contains(province)]
    print(df1[['date', 'Province', 'Total Positive', 'Today Positive',
               'Total Tested', '% Increase']].tail(nodays).dropna())

    df2 = df1[['date', 'Total Positive']].tail(nodays).dropna()
    df2.plot(x='date', y='Total Positive', kind='line')
    plt.show()

def covid_allpr(nodays):
    ##parsing data from the Canada covid stats
    data = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv', parse_dates=['date'], dayfirst=True)


    ##renaming columns to an intuitive names
    data.rename(columns={'prname': 'Province', "numtotal": "Total Positive", "numtoday": "Today Positive",
                         "numtested": "Total Tested", "percentoday": "% Increase"}, inplace=True)

    # data['date'] = data['date'].astype('datetime64')
    # data.sort_values('date')

    ##sorting by date
    data.sort_values('date')
    days = str(nodays) + 'D'

    ##filter out provincial data
    # for i in provinces:
    #     df1 = data[data['Province'].str.contains(i)]
    #     print(df1[['date', 'Province', 'Total Positive', 'Today Positive',
    #                'Total Tested', '% Increase']].tail(nodays).dropna())
    #
    #     df2 = df1[['date', 'Total Positive']].tail(nodays).dropna()
    #     df2.plot(x='date', y='Total Positive', kind='line', label = i)
    ##data.dropna()

    ##to print the table
    ##print(data[['date', 'Province', 'Total Positive']])

    ##to see datatypes in DF
    ##print(data.dtypes)

    ##creating a pivot and then plotting it
    df = data.pivot(index = "date", columns="Province", values="Total Positive")
    df = df.last(days)
    df.plot()

    df2 = data.pivot(index = "date", columns="Province", values="Today Positive")
    df2 = df2.last(days)
    df2.plot()
    plt.show()

def main():
    # covid()
    province = str(input("\nWhat province would you like to see data for? (enter all to see consolidated statistics or "
                         "Canada to see Canada-only statistics): "))

    if province == "all":
        nodays = int(input("For the past how many days?: "))
        covid_allpr(nodays)
    elif province not in provinces:
        print(province, "is not a valid province.")
        exit
    else:
        nodays = int(input("For the past how many days?: "))
        covid_pr(province, nodays)

main()