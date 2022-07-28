from .. import app, client, db
from datetime import datetime
from flask import flash, redirect, render_template, url_for, request
import pdb


@app.route('/report', methods=('GET', 'POST'))
def get_report():

    if request.method == 'GET':
        clients = db.clients.find()
        return render_template('/reports/query.html', clients=clients)

    sd = request.form['start_date']
    ed = request.form['end_date']
    start_date = datetime.strptime(sd, '%m/%d/%Y')
    end_date = datetime.strptime(ed, '%m/%d/%Y')
    
    client_id = int(request.form['client_id'])
    client_name = db.clients.find_one({'_id': client_id})['name']
    
    ''' I have to do this in two steps until I learn the right way'''
    cl = {'client': {'$eq': client_id}}
    dr = {'paid_date': {'$gte': start_date, '$lte': end_date}}
    aa = []
    aa.append(dr)
    aa.append(cl)
    bb = {'$and': aa}
    
    invoice_query = []
    invoice_query.append({'$match': bb})
    invoice_query.append({'$sort': {'paid_date': 1}})
    
    summary_query = [{'$match':  {'paid_date': {'$gte': start_date, '$lt': end_date }}} , 
                 {'$group':    {'_id': 'null',  'Amount': { '$sum': '$amount' },  'Hours': { '$sum': '$hours' } } } 
                ]
    
    invoices = db.invoice.aggregate(invoice_query)
    totals = db.invoice.aggregate(summary_query).next()
    
    return render_template('/reports/results.html', 
                           client_name=client_name, 
                           sd = sd, 
                           ed = ed,
                           items=invoices, totals=totals)
