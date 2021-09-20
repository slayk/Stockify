import requests
from datetime import date, timedelta
from twilio.rest import Client
import tweepy
from textblob import TextBlob
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from tkinter import *
from tkinter import messagebox

#Company details

# COMPANY_STOCKNAME = "IBM"
# COMPANY_NAME = "IBM"

# All API keys

consumer_key= 'your-consumer-key'
consumer_secret= 'your-consumer-secret'
access_token='your-access_token'
access_token_secret='your-access_token_secret'
NEWS_API_KEY = "your-NEWS-API-KEY"
STOCK_API_KEY = "your-STOCK_API_KEY"
account_sid = "your-account_sid"
auth_token = "your-auth-token"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function for swing traders

def SwingTrader():
    
    COMPANY_STOCKNAME = entry.get()
        # COMPANY_NAME = "IBM"
        # Getting hold of the dates
    try:
        if COMPANY_STOCKNAME == "":
            messagebox.showinfo(title="Error!", message="Please enter some company stock name.")
        print(COMPANY_STOCKNAME)
        today = date.today()
        yesterday = today - timedelta(days = 12)
        day_before_yesterday = today - timedelta(days = 13)

        # Getting hold of the required data for daily traders

        STOCK_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={COMPANY_STOCKNAME}&apikey={STOCK_API_KEY}"
        response_stock = requests.get(STOCK_URL)
        yesterday_stock_data = response_stock.json()["Time Series (Daily)"][str(yesterday)]["4. close"]
        day_before_yesterday_stock_data = response_stock.json()["Time Series (Daily)"][str(day_before_yesterday)]["4. close"]

    except KeyError:
        messagebox.showinfo(title="Warning!", message="API supports only company stocks of USA and Canada.")

    else:
        # Sentiment Analysis

        public_tweets = api.search(f'{COMPANY_STOCKNAME} stock')
        market_val = False
        threshold=0
        pos_sent_tweet=0
        neg_sent_tweet=0
        for tweet in public_tweets:
            analysis=TextBlob(tweet.text)
            if analysis.sentiment.polarity>=threshold:
                pos_sent_tweet=pos_sent_tweet+1
            else:
                neg_sent_tweet=neg_sent_tweet+1

        if pos_sent_tweet>neg_sent_tweet:
            market_val = True
        else:
            market_val = False

        # basic calculations

        difference = float(yesterday_stock_data)-float(day_before_yesterday_stock_data)
        if difference > 0:
            up_down = "📈"
        else:
            up_down = "📉"
        diff_percent = (difference/float(yesterday_stock_data))*100

        # If the change is there in the price, then SMS the user

        if abs(diff_percent) > 0.0004:
            news_params = {
                "apiKey": NEWS_API_KEY,
                "qInTitle": f"{COMPANY_STOCKNAME}",
            }
            NEWS_URL = "https://newsapi.org/v2/everything"
            response_news = requests.get(NEWS_URL, params=news_params)
            news_data = response_news.json()["articles"]
            three_art = news_data[:1]
            if market_val:
                formatted_list = [f"\nHELLO SWING TRADER!💰 \n{COMPANY_STOCKNAME}: {up_down}{round(diff_percent,4)}% \nAccording to Twitter Sentiment Analysis, the market for {COMPANY_STOCKNAME} is positive. You should definitely invest in the market.\n\nHeadline: {news_data['title']} \nBrief: {news_data['description']} \nContinue reading at {news_data['url']}\n\n" for news_data in three_art]
            else:
                formatted_list = [f"\nHELLO SWING TRADER!💰 \n{COMPANY_STOCKNAME}: {up_down}{round(diff_percent, 4)}% \nAccording to Twitter Sentiment Analysis, the market for {COMPANY_STOCKNAME} is negative so you should think twice before investing in the market.\n\nHeadline: {news_data['title']} \nBrief: {news_data['description']} \nContinue reading at {news_data['url']}\n\n" for news_data in three_art]
            for news_data in formatted_list:
                client = Client(account_sid, auth_token)
                message = client.messages \
                                .create(
                                    body=news_data,
                                    from_='from-number',
                                    to="to-number"
                                )
                print(message.status)

# Function for day traders

def DayTrader():
    COMPANY_STOCKNAME = entry.get()
    # COMPANY_NAME = "IBM"
    # Getting data for day traders

    try:
        print(COMPANY_STOCKNAME)
        if COMPANY_STOCKNAME == "":
            messagebox.showinfo(title="Error!", message="Please enter some company stock name.")
        ts = TimeSeries(key=STOCK_API_KEY, output_format = 'pandas')
        data, meta_data = ts.get_intraday(symbol=COMPANY_STOCKNAME, interval='1min', outputsize='full')

        close_data = data['4. close']
        percent_change = close_data.pct_change()

    except ValueError:
        messagebox.showinfo(title="Warning!", message="API supports only company stocks of USA and Canada.")

    else:
        # Sentiment Analysis

        public_tweets = api.search(f'{COMPANY_STOCKNAME} stock')
        market_val = False
        threshold=0
        pos_sent_tweet=0
        neg_sent_tweet=0
        for tweet in public_tweets:
            analysis=TextBlob(tweet.text)
            if analysis.sentiment.polarity>=threshold:
                pos_sent_tweet=pos_sent_tweet+1
            else:
                neg_sent_tweet=neg_sent_tweet+1

        if pos_sent_tweet>neg_sent_tweet:
            market_val = True
        else:
            market_val = False

        last_change = percent_change[-1]  
        if abs(last_change) > -10:
            news_params = {
                "apiKey": NEWS_API_KEY,
                "qInTitle": f"{COMPANY_STOCKNAME}",
            }
            NEWS_URL = "https://newsapi.org/v2/everything"
            response_news = requests.get(NEWS_URL, params=news_params)
            news_data = response_news.json()["articles"]
            three_art = news_data[:1]
            if market_val:
                formatted_list = [f"\nHELLO DAY TRADER!💰 \n{COMPANY_STOCKNAME}: 📈{round(last_change, 4)}% \nAccording to Twitter Sentiment Analysis, the market for {COMPANY_STOCKNAME} is positive. You should definitely invest in the market.\n\nHeadline: {news_data['title']} \nBrief: {news_data['description']} \nContinue reading at {news_data['url']}\n\n" for news_data in three_art]
            else:
                formatted_list = [f"\nHELLO DAY TRADER!💰 \n{COMPANY_STOCKNAME}: 📉{round(last_change,4)}% \nAccording to Twitter Sentiment Analysis, the market for {COMPANY_STOCKNAME} is negative so you should think twice before investing in the market.\n\nHeadline: {news_data['title']} \nBrief: {news_data['description']} \nContinue reading at {news_data['url']}\n\n" for news_data in three_art]
            for news_data in formatted_list:
                client = Client(account_sid, auth_token)
                message = client.messages \
                                .create(
                                    body=news_data,
                                    from_='from-number',
                                    to="to-number"
                                )
                print(message.status)

# Choose your trader type - Day Trader, Swing Trader

window = Tk()
window.title("STOCKIFY")
window.config(padx=10, pady=10, bg="#000000")
window.minsize(500, 650)

def AboutPop():
    messagebox.showinfo(title="About STOCKIFY", message="STOCKIFY is an upcoming stock market messaging application. We deliever you the latest stock market insights on the companies of your choice. Stock marketing is more than just exchanging, it includes strategical thinking, investment of hours and much more. \n\nHere are the types of traders we offer help: \nSwing Trader - Swing trading is a style of trading that attempts to capture short- to medium-term gains in a stock (or any financial instrument) over a period of a few days to several weeks. \nDay Trader - Day traders are traders who execute intraday strategies to profit off relatively short-lived price changes for a given asset. \n\nWIth every click, we offer you updates about the present stock increase or decrease or daily stock increase or decrease. You get additional news information on your favourite company and also, a Twitter Sentiment Analysis insight on whether you should invest in the market for the company or not.")

title_table = Label(text="STOCKIFY", font=("Courier", 25, "bold"), bg="#000000", fg="#93B5C6")
title_table.grid(row=0, column=1, columnspan=2)

canvas = Canvas(width = 450, height = 400, highlightthickness = 0)
back_img = PhotoImage(file = 'stock.png')
canvas.create_image(200, 200, image=back_img)
canvas.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

entry_label = Label(text="Enter the company stock name: ", bg="#000000", fg="#93B5C6", font=("Courier", 10))
entry_label.grid(row=3, column=1, padx=10, pady=10)

entry = Entry(width = 30)
entry.grid(row=3, column=2, padx=10, pady=10)

day_button = Button(text = "Day Trader", width = 16, bg="#150050", fg="#F7F6F2", command=DayTrader)
day_button.grid(row=4, column=1, padx=10, pady=10)

swing_button = Button(text = "Swing Trader", width = 16, bg="#150050", fg="#F7F6F2", command=SwingTrader)
swing_button.grid(row=4, column=2, padx=10, pady=10)

about_button = Button(text="About", font = ("Courier", 10, "bold"), bg="#150050", fg="#F7F6F2", width=35, command=AboutPop)
about_button.grid(row=2, column=0, columnspan=3, padx=8, pady=8)

end_label = Label(text = "Made by SlayK", font = ("Courier", 10, "bold"), bg="#000000", fg="#93B5C6")
end_label.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

window.mainloop()
