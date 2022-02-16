import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt


def main():
    stocks = pd.read_csv('stocks.csv')['ticker']

    # scrape last 10 years of ticker data
    end_date = datetime.date.today()
    start_date = end_date - relativedelta(years=10)
    tickers = {}
    for stock in stocks:
      tickers[stock] = web.DataReader(stock,'yahoo',start_date, end_date)

    # scrape dividends, calc avg
    divs = {}
    divsums = {}
    for stock in stocks:
      divs[stock] = web.DataReader(stock, 'yahoo-dividends', start_date, end_date)
      divsums[stock] = round(divs[stock]['value'].sum(),2)

    # get closes and convert to %change, calc final %
    close_last = {}
    close_pct = {}
    finalpct = {}
    for stock in stocks:
      close_last[stock] = tickers[stock]['Adj Close'][0]
      close_pct[stock] = 100*(tickers[stock]['Adj Close']/close_last[stock]-1)
      finalpct[stock] = close_pct[stock][-1].round(2)

    # plot
    plt.style.use('default')
    plt.figure(figsize=(16, 8), dpi=150)
    for stock in stocks:
      close_pct[stock].plot(label=f'{stock}: {finalpct[stock]}% {close_last[stock].round(2)}+{divsums[stock]}divs')

    plt.title('PCT Change')
    plt.xlabel('Date')
    plt.legend()
    plt.savefig(f'{"_".join(stocks)}.png')


if __name__ == "__main__":
    main()
