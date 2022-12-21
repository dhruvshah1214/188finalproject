from source.db import db

from source.db.models.monitor import Monitor
from source.db.models.target import Target
from source.db.models.user import User

import os

import requests
from bs4 import BeautifulSoup

import diff_match_patch.diff_match_patch as dmp

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

differ = dmp()

enabled_monitors = db.query(Monitor).join(Target).filter(Monitor.enabled == True).distinct(Target.id).all()
targets = [monitor.target for monitor in enabled_monitors]
target_tuples = [(target.id, target.url, target.selector) for target in targets]

print(f"Targets diffing: {target_tuples}")

diffs = {}

for id, url, selector in target_tuples:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.select(selector)[0].text
    print(f"FETCHED TARGET {result}")

    path = os.path.join("/app/storage", id)
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = file.read()
            print(f"CURRENT DATA: {data}")
            if data.strip() != result.strip():
                diff_objs = differ.diff_main(data, result)
                html = differ.diff_prettyHtml(diff_objs)
                diffs[str(id)] = str(html)
    with open(path, "w") as file:
        file.write(str(result))

print(diffs)

print(os.environ.get('SENDGRID_API_KEY'))
sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

for monitor in enabled_monitors:
    if monitor.target.id not in diffs.keys():
        continue
    email = monitor.user.email
    diff_html = diffs[monitor.target.id]
    print(f"Sending email to {email} with diff html {diff_html}")

    message = Mail(from_email=From('dhruv.shah@gmail.com', 'cpmonitor-188'),
                to_emails=To(email),
                subject=Subject(f"Monitor {monitor.name} has fired!"),
                plain_text_content=PlainTextContent(diff_html),
                html_content=HtmlContent(diff_html))
    
    # Get a JSON-ready representation of the Mail object
    mail_json = message.get()
    print(mail_json)
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
