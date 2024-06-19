import smtplib
import datetime as dt
from random import choice

my_email = "abc@gmail.com"  # fill in your email address
recipient_mail = "xyz@gmail.com"  # fill the recipient mail
my_pass = "xxxx xxxx xxxx xxxx"  # enter the valid 16 digit app password

# date time adjustment and checking
current_time = dt.datetime.now()
day_of_week = current_time.weekday()
if day_of_week == 0:
    with open("quotes.txt") as quote_file:
        value = quote_file.readlines()
        quote = choice(value)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_pass)
        connection.sendmail(from_addr=my_email,
                            to_addrs=recipient_mail,
                            msg=f"Subject:Monday Motivation\n\n{quote}"
                            )
