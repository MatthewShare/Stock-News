import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = os.environ["ENV-API_KEY"]
NEWS_API_KEY = os.environ["ENV-NEWS_API_KEY"]
account_sid = os.environ["ENV-SID"]
auth_token = os.environ["ENV-AUTH"]

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": API_KEY
}
response = requests.get("https://www.alphavantage.co/query", params=parameters)
data = response.json()

news_parameters = {
    "q": COMPANY_NAME,
    "from": "2024-04-01",
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}
news_response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
news_data = news_response.json()

dictionary_days = data["Time Series (Daily)"]
day_before_yesterday = float(list(dictionary_days.items())[1][1]["4. close"])
yesterday = float(list(dictionary_days.items())[0][1]["4. close"])
three_days_ago_date = list(dictionary_days.items())[1][0]
percentage_change = (yesterday - day_before_yesterday) / day_before_yesterday

if abs(percentage_change) > 0.05:
    client = Client(account_sid, auth_token)
    if percentage_change < 0:
        message = client.messages.create(
            body=f"Tesla has had{abs(percentage_change)}% Decrease.",
            from_="+447445046632",
            to="+447436120966"
        )
    else:
        message = client.messages.create(
            body=f"Tesla has had a{abs(percentage_change)}% Increase.",
            from_="+447445046632",
            to="+447436120966"
        )
    for number in range(0, 3):
        message = client.messages.create(
            body=f"{news_data["articles"][number]["title"]} : {news_data["articles"][number]["description"]}",
            from_="+447445046632",
            to="+447436120966"
        )
