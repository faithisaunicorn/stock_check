import os
import requests
from twilio.rest import Client
import datetime

TWILIO_ACCOUNT_SID = "X"
TWILIO_AUTH_TOKEN = "X"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "E5A5R1N7VO8XA57A"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_API_KEY = "574577ebdeda47748093d968d46e48ed"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 
response_stock = requests.get(f"{STOCK_ENDPOINT}?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&apikey={STOCK_API_KEY}")
response_stock.raise_for_status()
stock_data = response_stock.json()["Time Series (Daily)"]
stock_list = [value for (key, value) in stock_data.items()] #list comprehension
stock_data_ytd = float(stock_list[0]["4. close"])
stock_data_ytdytd = float(stock_list[1]["4. close"])
print(stock_data_ytd)
print(stock_data_ytdytd)

daily_change = (stock_data_ytd)-(stock_data_ytdytd)
perc_change = round(((abs((daily_change)/(stock_data_ytd)))*100),2)
print(perc_change)

if daily_change>=0:
    up_down = f"🔺{perc_change}%"
if daily_change<0:
    up_down = f"🔻{perc_change}%"

## STEP 2: Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
# https://newsapi.org/v2/everything?q=TSLA&apiKey=574577ebdeda47748093d968d46e48ed
#HINT 1: Think about using the Python Slice Operator
if perc_change >= 3: #changed to 3 for testing purposes
    response = requests.get(f"{NEWS_ENDPOINT}?q={STOCK}&apiKey={NEWS_API_KEY}")
    response.raise_for_status()
    news_data = response.json()
    news_data_slice = news_data["articles"][:3]
    print(news_data_slice)

## STEP 3
# Send a separate message with each article's title and description to your phone number. Use list comprehension
format = [f"""{STOCK}: {up_down}
Headline: {article['title']}
Brief: {article['description']}""" for article in news_data_slice]
print(format)

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

message = client.messages.create(
  body=f"{format}",
  from_="X",
  to="X"
)

print(message.sid)
