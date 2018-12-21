import requests
import json
import csv
from models import StockData, StockMD
from app import db
import sys


def scrape(sym):
    print("Scraping data for " + sym)

    # Default values
    current_price = None
    percent_diff_mean = None
    analyst_rating = None
    number_of_analysts = 0

    stock = StockData.query.filter_by(symbol=sym).first()

    try:
        url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?" \
              "formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%" \
              "2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatist" \
              "ics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(sym)
        page = requests.get(url, verify=False)
        data = json.loads(page.text)

        # Primary Statistics
        current_price = data["quoteSummary"]["result"][0]["financialData"]["currentPrice"]['raw']
        target_price_low = data["quoteSummary"]["result"][0]["financialData"]["targetLowPrice"]['raw']
        target_price_mean = data["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
        target_price_high = data["quoteSummary"]["result"][0]["financialData"]["targetHighPrice"]['raw']
        analyst_rating = data["quoteSummary"]["result"][0]["financialData"]["recommendationMean"]['raw']
        number_of_analysts = data["quoteSummary"]["result"][0]["financialData"]["numberOfAnalystOpinions"]['raw']

        # Secondary Statistics
        percent_diff_low = (target_price_low - current_price) / current_price
        percent_diff_mean = (target_price_mean - current_price) / current_price
        percent_diff_high  = (target_price_high - current_price) / current_price
        target_spread = percent_diff_high - percent_diff_low

    except (KeyError, TypeError):
        print("Forecast data not available.")

    finally:
        # Update Database:
        if stock is None:
            data_entry = StockData(symbol=sym,
                                   price=current_price,
                                   mean_price_target_diff=percent_diff_mean,
                                   mean_analyst_rating=analyst_rating,
                                   n=number_of_analysts)

            db.session.add(data_entry)
        else:
            stock.price = current_price
            stock.mean_price_target_diff = percent_diff_mean
            stock.mean_analyst_rating = analyst_rating
            stock.n = number_of_analysts


def get_market_data():
    print("Fetching market data...")
    exchanges = ['NASDAQ', 'NYSE', 'AMEX']
    for exchange in exchanges:
        print("Exchange: " + exchange)
        url = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange={}&render=download'.format(exchange)
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            company_list = list(cr)
            for row in company_list[1:]:
                sym = row[0].strip()
                if sym.isalpha():
                    stock_metadata = StockMD.query.filter_by(symbol=sym).first()
                    if stock_metadata is None:
                        name = row[1].strip()
                        sector = row[6].strip()
                        metadata_entry = StockMD(symbol=sym,
                                                 name=name,
                                                 sector=sector)

                        db.session.add(metadata_entry)

                    scrape(sym)

        db.session.commit()

    print("Market data updated.")


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    try:
        while True:
            get_market_data()
    except KeyboardInterrupt:
        sys.exit(0)
