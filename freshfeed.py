#!/usr/bin/python

import requests, os
from flask import Flask, render_template

MAX_TICKETS_PER_PAGE = 30

app = Flask(__name__)

domain = os.environ['FRESHDESK_DOMAIN']
username = os.environ['FRESHDESK_USERNAME']
password = os.getenv('FRESHDESK_PASSWORD', 'X')
url="http://%s/helpdesk/tickets/filter/all_tickets?format=json" % (domain)

@app.route("/")
def do_tickets():
    tickets = []
    more_tickets = True
    page = 1
    while more_tickets:
        r = requests.get("%s&page=%d" % (url, page), auth=(username, password))
        new_tickets = r.json()
        tickets.extend(new_tickets)
        if len(new_tickets) < MAX_TICKETS_PER_PAGE:
            more_tickets = False
        page += 1


    for ticket in tickets:
        if ticket['status_name'] != 'Open':
            tickets.remove(ticket)

    def weight(ticket):
        return -ticket['priority'], -ticket['display_id']


#        print i
#        print "%d, %s, %d, %s, %d, %s, %s" % (i['display_id'], i['subject'], i['status'], i['status_name'], i['priority'], i['priority_name'], i['responder_name'])
    return render_template('template.html', tickets=sorted(tickets, key=weight))

if __name__ == "__main__":
    app.run(debug=True)
