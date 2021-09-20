# Stockify

**About Stockify:**

Stockify is a messaging application. You can get latest insights into the stock market of the company you invested in. The application supports two trader types:

- Swing Trader -> Swing trading is a style of trading that attempts to capture short- to medium-term gains in a stock (or any financial instrument) over a period of a few days to several weeks. Swing traders primarily use technical analysis to look for trading opportunities.
- Day Trader -> Day traders are traders who execute intraday strategies to profit off relatively short-lived price changes for a given asset.

You enter the name of the company you have invested in or want to invest in. Select what type of trading style you want to follow(Day-Trading or Swing-Trading) and the following information and data will be messaged to you on your number:

- Percentage Change (different for Day-Trader and Swing-Trader)
- Twitter Sentiment Analysis Report
  - If the sentiment analysis of the tweets are overall positive, then the application will suggest you to invest in the market for the company.
  - If the sentiment analysis of the tweets are overall negative, then the application will suggest you not to invest in the market for the company.
- Shares a news related to the company - Headline, Brief and the whole news link. The number of news received can be altered in the program.


***Here's the User Interface of the Stockify Application:***

![front](https://user-images.githubusercontent.com/68421513/133963429-d969c97e-5c59-48c0-9399-87b703b01366.jpg)

---

**Modules used:** 

- requests
- datetime
- twilio.rest
- tweepy
- textblob
- pandas
- alpha_vantage.timeseries
- tkinter

---

**APIs used:**

- Alphavantage ( For Fetching Stock Data ) 
  - Read about it and generate your API key, here: https://www.alphavantage.co/
- News API (For Fetching News Data )
  - Read about it and generate your API key, here: https://newsapi.org/
- Tweepy ( For fetching Tweets )
  - Read about it and generate your consumer key, consumer secret, access token and access token secret, here: https://www.tweepy.org/
- Twilio ( For Messaging )
  - Read about it and generate your account sid and auth token, here: https://www.twilio.com/

---

***Stats Recevied By A Day Trader:***

***Company Chosen: IBM***

![IBM_Day](https://user-images.githubusercontent.com/68421513/133965096-bf1c92ea-4e5a-4c53-9c22-61bc4a00611c.jpg)


***Stats Recevied By A Swing Trader:***

***Company Chosen: APPL***

![APPL_Swing](https://user-images.githubusercontent.com/68421513/133965497-402492d4-52cd-4bab-9cc8-1060c67e7608.jpg)

