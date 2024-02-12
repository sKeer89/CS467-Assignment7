import csv
import mailbox

mbox_file_path = "/Users/XXX/Downloads/Takeout/Mail/IP.mbox"
output_csv_file = "output.csv"

with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Subject', 'From', 'To'])
    for message in mailbox.mbox(mbox_file_path):
        date = message['Date']
        subject = message['Subject']
        sender = message['From']
        recipient = message['To'] if 'To' in message else ''
        writer.writerow([date, subject, sender, recipient])