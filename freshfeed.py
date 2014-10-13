#!/usr/bin/python

import requests, os
from flask import Flask, render_template, redirect, url_for

MAX_TICKETS_PER_PAGE = 30

#these are site-specific; change as required
TICKET_VIEW_OPEN="313844"
TICKET_VIEW_READY_FOR_COLLECTION="314401"

app = Flask(__name__)

domain = os.environ['FRESHDESK_DOMAIN']
username = os.environ['FRESHDESK_USERNAME']
password = os.getenv('FRESHDESK_PASSWORD', 'X')
tickets = []


def get_tickets(view=None):
    if view:
        url = "http://%s/helpdesk/tickets/view/%s?format=json" % (domain, view)
    else:
        url = "http://%s/helpdesk/tickets/filter/all_tickets?format=json" % (domain)
    all_tickets = []
    more_tickets = True
    page = 1

    while more_tickets:
        r = requests.get("%s&page=%d" % (url, page), auth=(username, password), headers={'content-type': 'application/json'})
        new_tickets = r.json()
        all_tickets.extend(new_tickets)
        if len(new_tickets) < MAX_TICKETS_PER_PAGE:
            more_tickets = False
        page += 1
    return all_tickets


@app.route("/")
def index():
    return redirect(url_for('do_tickets'))


@app.route("/tickets")
def do_tickets():
    display_tickets = []

    for ticket in get_tickets(TICKET_VIEW_OPEN):
        if ticket['status_name'] == 'Open':
            display_tickets.append(ticket)

    def weight(ticket):
        return -ticket['priority'], -ticket['display_id']

    return render_template('tickets.html', tickets=sorted(display_tickets, key=weight))


@app.route("/awaiting_collection")
def do_awaiting_collection():
    display_tickets = []

    for ticket in get_tickets(TICKET_VIEW_READY_FOR_COLLECTION):
        if ticket['status_name'] == 'Ready For Collection':
            display_tickets.append(ticket)

    def weight(ticket):
        return -ticket['display_id']

    return render_template('awaiting_collection.html', tickets=sorted(display_tickets, key=weight))


if __name__ == "__main__":
    app.run(debug=True)
