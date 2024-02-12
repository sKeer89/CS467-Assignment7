import pandas as pd
import re
from dateutil import parser
df = pd.read_csv("output.csv")
def extract_email(raw_email):
    email_pattern = r'\b[A-Za-z0-9._%+-]*[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(email_pattern, raw_email)
    if emails:
        return emails[0]
    else:
        return None

def clean_recipients(recipients_str):
    if pd.isnull(recipients_str):
        return []
    else:
        filtered_recipients = []
        recipients_list = re.split(r',\s*', recipients_str)
        cleaned_recipients = [extract_email(recipient) for recipient in recipients_list]
        for r in cleaned_recipients:
            #Considering only people email IDs and not the mails from brands or linkedIn, etc.
            if r and ("@gmail" in r or "@meta" in r or "@yahoo" in r or "@illinois" in r):
                filtered_recipients.append(r)
        return filtered_recipients 
        return [recipient for recipient in cleaned_recipients if recipient]
    

df['To'] = df['To'].apply(clean_recipients)
df['To'] = df['To'].apply(lambda x: [email.lower() for email in x])
df['From'] = df['From'].apply(clean_recipients)
df['From'] = df['From'].apply(lambda x: [email.lower() for email in x])
'''
recipient_counts = df.explode('To')['To'].value_counts()
from_counts = df.explode('From')['From'].value_counts()
print(recipient_counts, from_counts)  
'''

def extract_date_month_year(date_str):
    length = 31
    date_str = date_str[:length].strip()
    parsed_date = parser.parse(date_str)
    #print(parsed_date.day, parsed_date.month, parsed_date.year)
    return (parsed_date.day, parsed_date.month, parsed_date.year)

df['Date_Month_Year'] = df['Date'].apply(extract_date_month_year)
df.to_csv("cleaned_temp.csv", index=False)

#Q1: People I have emailed in the month of January 2024
condition = any((row[1] == 1 and row[2] == 2024) for row in df['Date_Month_Year'])
if condition:
    filtered_df = df[df['Date_Month_Year'].apply(lambda x: (x[1] == 1 and x[2]) == 2024)]
    result = filtered_df.explode('To')['To'].value_counts()
    print(result[:15])
else:
    print("No entries exist")

print('--------------------------------------------------------------------------------------')
#Q2: People who emailed me in the month of January 2024
condition = any((row[1] == 1 and row[2] == 2024) for row in df['Date_Month_Year'])
if condition:
    filtered_df = df[df['Date_Month_Year'].apply(lambda x: (x[1] == 1 and x[2]) == 2024)]
    result = filtered_df.explode('From')['From'].value_counts()
    print(result[:15])
else:
    print("No entries exist")

print('--------------------------------------------------------------------------------------')

#Q3: People I have emailed in the year of 2023
condition = any((row[2] == 2023) for row in df['Date_Month_Year'])
if condition:
    filtered_df = df[df['Date_Month_Year'].apply(lambda x: (x[2]) == 2023)]
    result = filtered_df.explode('To')['To'].value_counts()
    print(result[:15])
else:
    print("Condition not satisfied.")

print('--------------------------------------------------------------------------------------')

#Q4: People who have emailed me in the year of 2023
condition = any((row[2] == 2023) for row in df['Date_Month_Year'])
if condition:
    filtered_df = df[df['Date_Month_Year'].apply(lambda x: (x[2]) == 2023)]
    result = filtered_df.explode('From')['From'].value_counts()
    print(result[:15])
else:
    print("Condition not satisfied.")