import smtplib
import requests as reqs
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_PRICE_URL = "https://www.alphavantage.co/query?"
STOCK_API_KEY = "YOUR STOCK API KEY"

# NewsAPI details
NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "NEWS API KEY"

# Twilio Details
account_sid = "Twilio Acc SID"
auth_key = "Twilio Auth key"

# Mailing Details
mail_id = "xyz@gmail.com"
password = "16 digit key"

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
st_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

response = reqs.get(url=STOCK_PRICE_URL, params=st_parameter)
response.raise_for_status()
data_set = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data_set.items()]

most_recent_closing_price = float(data_list[0]["4. close"])
previous_closing_price = float(data_list[1]["4. close"])

difference = round(((most_recent_closing_price - previous_closing_price) / most_recent_closing_price) * 100, 2)

if difference < 0:
    diff_with_symbol = f"🔻{difference}%"
else:
    diff_with_symbol = f"🔺{difference}%"

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if difference >= 5 or difference <= -5:
    news_parameter = {
        "q": "tesla",
        "searchIn": "title",
        "from": "2024-06-11",
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 3,
        "apiKey": NEWS_API_KEY
    }

    news_response = reqs.get(url=NEWS_API_URL, params=news_parameter)
    news_response.raise_for_status()
    content = news_response.json()

    top_news = content["articles"]

    # STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.

    # Optional: Format the SMS message like this:
    """
    TSLA: 🔺2%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
    file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
    near the height of the coronavirus market crash.
    or
    "TSLA: 🔻5%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
    file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
    near the height of the coronavirus market crash.
    """

    for news in top_news:
        headline = news["title"]
        brief = news["description"]
        text_msg = f"""{STOCK}: {diff_with_symbol}\n
                    Headline: {headline}\n
                    Brief: {brief}"""
        client = Client(account_sid, auth_key)
        message = client.messages.create(from_="mob num",
                                         to="recipient number",
                                         body=text_msg)

        # Also send an email
        with smtplib.SMTP("smtp.gmail.com") as connection:
            text_msg_utf8 = text_msg.encode("utf-8")

            # Decode text_msg_utf8 back to string
            text_msg_str = text_msg_utf8.decode('utf-8')

            # Email Confi
            subject = "Tesla Stock Price Tracker"
            from_addr = mail_id
            to_addrs = mail_id

            # Construct the email message
            msg = MIMEMultipart()
            msg["From"] = from_addr
            msg["To"] = to_addrs
            msg["Subject"] = subject

            # Add the UTF encoded msg to the body
            msg.attach(MIMEText(text_msg_str, "plain", "utf-8"))

            connection.starttls()
            connection.login(user=mail_id, password=password)
            connection.sendmail(from_addr=mail_id, to_addrs=mail_id, msg=msg.as_string())
