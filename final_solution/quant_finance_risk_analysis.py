# -*- coding: utf-8 -*-

!pip install yfinance

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

price_history = yf.Ticker('TSLA').history(period='2y', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                   interval='1d', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                   actions=False)

price_history

def find_volatility(ticker):
  data = yf.Ticker(ticker).history(period='3mo', interval='1d', actions=False)
  data['Log returns'] = np.log(data['Close']/data['Close'].shift())
  volatility = data['Log returns'].std()*252**.5
  return volatility

def find_beta_against_spy(ticker):
  data = yf.Ticker(ticker).history(period='12mo', interval='1d', actions=False)
  data['Log returns'] = np.log(data['Close']/data['Close'].shift())
  data_spy = yf.Ticker('SPY').history(period='12mo', interval='1d', actions=False)
  data_spy['Log returns'] = np.log(data_spy['Close']/data_spy['Close'].shift())
  cov = data['Log returns'].cov(data_spy['Log returns'])
  var = data_spy['Log returns'].var()
  beta_spy = cov/var
  return beta_spy

def find_beta_against_iwm(ticker):
  data = yf.Ticker(ticker).history(period='12mo', interval='1d', actions=False)
  data['Log returns'] = np.log(data['Close']/data['Close'].shift())
  data_iwm = yf.Ticker('iwm').history(period='12mo', interval='1d', actions=False)
  data_iwm['Log returns'] = np.log(data_iwm['Close']/data_iwm['Close'].shift())
  cov = data['Log returns'].cov(data_iwm['Log returns'])
  var = data_iwm['Log returns'].var()
  beta_iwm = cov/var
  return beta_iwm

def find_beta_against_dia(ticker):
  data = yf.Ticker(ticker).history(period='12mo', interval='1d', actions=False)
  data['Log returns'] = np.log(data['Close']/data['Close'].shift())
  data_dia = yf.Ticker('dia').history(period='12mo', interval='1d', actions=False)
  data_dia['Log returns'] = np.log(data_dia['Close']/data_dia['Close'].shift())
  cov = data['Log returns'].cov(data_dia['Log returns'])
  var = data_dia['Log returns'].var()
  beta_dia = cov/var
  return beta_dia

def find_average_weekly_drawdown(ticker):
  data = yf.Ticker(ticker).history(period='12mo', interval='1d', actions=False)
  avg_weekly_drawdown = (data['Close'].min() - data['Close'].max())/data['Close'].max()
  return avg_weekly_drawdown

def find_maximum_weekly_drawdown(ticker):
  data = yf.Ticker(ticker).history(period='12mo', interval='1d', actions=False)
  avg_maximum_drawdown = (data['Close'].min() - data['Close'].max())/data['Close'].max()
  return avg_maximum_drawdown

def find_return(ticker):
  data = yf.Ticker(ticker).history(period='10y', interval='3mo', actions=False)
  ret = ((data['Close'].iloc[-1] - data['Close'].iloc[0])/data['Close'].iloc[0])
  return ret

def find_annualized_return(ticker):
  data = yf.Ticker(ticker).history(period='10y', interval='3mo', actions=False)
  ret = ((data['Close'].iloc[-1] - data['Close'].iloc[0])/data['Close'].iloc[0])
  annualized_ret = ((1+ret)**(1/10)) - 1
  return annualized_ret

tickers = ['TSLA', 'AAPL', 'MSFT', 'AMZN', 'UNH', 'GOOGL', 'NVDA']

table1 = pd.DataFrame(columns=['Ticker', 'Portfolio Weight (equally weighted)', 'Annualized Volatility (using trailing 3-months)', 'Beta against SPY (using trailing 12-months)', 'Beta against IWM (using trailing 12-months)', 'Beta against DIA (using trailing 12-months)', 'Average Weekly Drawdown (52-week Low minus 52-week High) / 52-week High', 'Maximum Weekly Drawdown (52-week Low minus 52-week High) / 52-week High', 'Total Return (using trailing 10-years)', 'Annualized Total Return (using trailing 10-years)'])

table1['Ticker'] = tickers
table1['Portfolio Weight (equally weighted)'] = [1.0 for i in range(len(tickers))]
table1['Annualized Volatility (using trailing 3-months)'] = list(map(find_volatility, tickers))
table1['Beta against SPY (using trailing 12-months)'] = list(map(find_beta_against_spy, tickers))
table1['Beta against IWM (using trailing 12-months)'] = list(map(find_beta_against_iwm, tickers))
table1['Beta against DIA (using trailing 12-months)'] = list(map(find_beta_against_dia, tickers))
table1['Average Weekly Drawdown (52-week Low minus 52-week High) / 52-week High'] = list(map(find_average_weekly_drawdown, tickers))
table1['Maximum Weekly Drawdown (52-week Low minus 52-week High) / 52-week High'] = list(map(find_maximum_weekly_drawdown, tickers))
table1['Total Return (using trailing 10-years)'] = list(map(find_return, tickers))
table1['Annualized Total Return (using trailing 10-years)'] = list(map(find_annualized_return, tickers))

table1.head(len(tickers))

etfs = ['EWD', 'SLX', 'CQQQ']

df = yf.Ticker(tickers[0]).history(period='10y', interval='1d', actions=False)['Close']
for t in tickers[1:]:
  df = df + yf.Ticker(t).history(period='10y', interval='1d', actions=False)['Close']

df.head()

df.tail()

df/=len(tickers)

df.tail()

def find_etf_correlation(ticker):
  data = yf.Ticker(ticker).history(period='10y', interval='1d', actions=False)['Close']
  corr = data.corr(df)
  return corr

def find_etf_covariance(ticker):
  data = yf.Ticker(ticker).history(period='10y', interval='1d', actions=False)['Close']
  cov = data.cov(df)
  return cov

def find_etf_tracking_errors(ticker):
  data = yf.Ticker(ticker).history(period='10y', interval='1d', actions=False)['Close']
  tracking_error = np.std((df.values - data.values) / df.values)
  return tracking_error

def find_etf_sharpe_ratio(ticker):
  data = yf.Ticker(ticker).history(period='10y', interval='1d', actions=False)['Close'].pct_change().dropna()
  data = data.values
  risk_free_Rate = 0.0
  mean_daily_return = sum(data)/len(data)
  std = np.std(data)
  daily_sharpe_ratio = (mean_daily_return - risk_free_Rate) / std
  sharpe_ratio = 252**(1/2) * daily_sharpe_ratio
  return sharpe_ratio

def find_etf_annualized_volatility_spread(ticker):
  data = yf.Ticker(ticker).history(period='10y', interval='1d', actions=False)
  data['Log returns'] = np.log(data['Close']/data['Close'].shift())
  etf_volatility = data['Log returns'].std()*252**.5
  portfolio_log_returns = np.log(df/df.shift())
  portfolio_volatility = portfolio_log_returns.std()*252**.5
  return portfolio_volatility - etf_volatility

table2 = pd.DataFrame(columns=['ETF Ticker', 'Correlation against ETF', 'Covariance of Portfolio against ETF', 'Tracking Errors (using trailing 10-years)', 'Sharpe Ratio (using current risk-free rate)', 'Annualized Volatility (252 days) Spread (Portfolio Volatility ??? ETF Volatility)'])

table2['ETF Ticker'] = etfs
table2['Correlation against ETF'] = list(map(find_etf_correlation, etfs))
table2['Covariance of Portfolio against ETF'] = list(map(find_etf_covariance, etfs))
table2['Tracking Errors (using trailing 10-years)'] = list(map(find_etf_tracking_errors, etfs))
table2['Sharpe Ratio (using current risk-free rate)'] = list(map(find_etf_sharpe_ratio, etfs))
table2['Annualized Volatility (252 days) Spread (Portfolio Volatility ??? ETF Volatility)'] = list(map(find_etf_annualized_volatility_spread, etfs))

table2.head()

table3 = pd.DataFrame()
table3['EquallyWeightedPortfolio'] = df
correlation_matrix_tickers = etfs + tickers
for t in correlation_matrix_tickers:
  table3[t] = yf.Ticker(t).history(period='10y', interval='1d', actions=False)['Close']

table3.corr()

table3.head()

