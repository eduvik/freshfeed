# !/usr/bin/python

import requests, os
from flask import Flask, render_template, redirect, url_for

MAX_TICKETS_PER_PAGE = 30

app = Flask(__name__)

domain = os.environ['FRESHDESK_DOMAIN']
username = os.environ['FRESHDESK_USERNAME']
password = os.getenv('FRESHDESK_PASSWORD', 'X')
url = "http://%s/helpdesk/tickets/filter/all_tickets?format=json" % (domain)
tickets = []


def get_all_tickets():
    all_tickets = []
    more_tickets = True
    page = 1

    while more_tickets:
        r = requests.get("%s&page=%d" % (url, page), auth=(username, password))
        new_tickets = r.json()
        all_tickets.extend(new_tickets)
        if len(new_tickets) < MAX_TICKETS_PER_PAGE:
            more_tickets = False
        page += 1
    return all_tickets


@app.route("/")
def index():
    return redirect(url_for('tickets'))


@app.route("/tickets")
def do_tickets():
    display_tickets = []

    for ticket in get_all_tickets():
        if ticket['status_name'] == 'Open':
            display_tickets.append(ticket)

    def weight(ticket):
        return -ticket['priority'], -ticket['display_id']

    return render_template('tickets.html', tickets=sorted(display_tickets, key=weight))


@app.route("/awaiting_collection")
def do_awaiting_collection():
    display_tickets = []

    for ticket in get_all_tickets():
        if ticket['status_name'] == 'Resolved' and ticket['custom_field']['cf_device_submitted_1956']:
            display_tickets.append(ticket)

    def weight(ticket):
        return -ticket['priority'], -ticket['display_id']

    return render_template('awaiting_collection.html', tickets=sorted(display_tickets, key=weight))


if __name__ == "__main__":
    app.run(debug=True)
