from .. import app, client, db
from datetime import datetime
from flask import flash, redirect, render_template, url_for, request
import pdb


@app.route('/report', methods=('GET', 'POST'))
def get_report():

    clients = db.clients.find()
    if request.method == 'GET':
        return render_template('/reports/query.html', clients=clients, error=False)
    
    sd = request.form['start_date']
    ed = request.form['end_date']
    
    try:
        start_date = datetime.strptime(sd, '%m/%d/%Y')
        end_date = datetime.strptime(ed, '%m/%d/%Y')
        if start_date > end_date:
            return render_template('/reports/query.html', clients=clients, error=True)    
    except ValueError:
        return render_template('/reports/query.html', clients=clients, error=True)
    
    client_id = int(request.form['client_id'])
    client_name = db.clients.find_one({'_id': client_id})['name']
    
    ''' I have to do this in two steps until I learn the right way'''
    cl = {'client': {'$eq': client_id}}
    dr = {'paid_date': {'$gte': start_date, '$lte': end_date}}
    sg = {'$group': {'_id': 'null', 'Amount': {'$sum': '$amount'}, 'Hours': {'$sum': '$hours'}}}
    aa = []
    aa.append(cl)
    aa.append(dr)
    bb = {'$and': aa}
    
    invoice_query = []
    invoice_query.append({'$match': bb})
    invoice_query.append({'$sort': {'paid_date': 1}})
    
    summary_query = []
    summary_query.append({'$match': bb})
    summary_query.append(sg)
    
    invoices = db.invoice.aggregate(invoice_query)
    tmp = [i for i in invoices]
 
    try:
        totals = db.invoice.aggregate(summary_query).next()
    except StopIteration:
        totals = 'none'
    
    return render_template('/reports/results.html', 
                           client_name=client_name, 
                           error=False,
                           sd = sd, 
                           ed = ed,
                           items=invoices, totals=totals)
