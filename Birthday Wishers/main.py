import os
import datetime as dt
import pandas as pd
import random
import smtplib

recip_name = ""
recip_email_id = ""

# Current date manipulation
current_date = dt.datetime.now()

month = current_date.month
day = current_date.day

# Reading CSV and extracting data
birthday_file = pd.read_csv("birthdays.csv")
content = birthday_file.to_dict(orient="records")

# Verification of records from the current date
for record in content:
    if record["month"] == month and record["day"] == day:
        recip_name = record["name"]
        recip_email_id = record["email"]
        # Picking up random email template
        files = os.listdir("letter_templates/")

        txt_files = [file for file in files if file.endswith(".txt")]
        random_letter = random.choice(txt_files)

        # Renaming the [NAME] with the actual recipient
        with open(f"letter_templates/{random_letter}", "r") as chosen_template:
            email_content = chosen_template.read()

        final_content = email_content.replace("[NAME]", recip_name)

        # The mailing procedure
        my_email = "xyz@gmail.com"
        my_pw = "zzzz zzzz zzzz zzzz"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_pw)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject:Birthday Wishes {recip_name}\n\n"
                                                                           f"{final_content}")
    else:
        print(f"No records found for the month {month} and day {day}")


