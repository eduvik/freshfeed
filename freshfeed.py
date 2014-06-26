#!/usr/bin/python

import requests, os
from flask import Flask, render_template
app = Flask(__name__)

domain = os.environ['FRESHDESK_DOMAIN']
username = os.environ['FRESHDESK_USERNAME']
password = os.getenv('FRESHDESK_PASSWORD', 'X')
url="http://%s/helpdesk/tickets/filter/all_tickets?format=json" % (domain)

@app.route("/")
def do_tickets():
    r=requests.get(url, auth=(username, password))

    tickets = r.json()
    return render_template('template.html', tickets=tickets)

if __name__ == "__main__":
    app.run()