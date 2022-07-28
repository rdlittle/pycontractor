from .. import app, client, db
from datetime import datetime
from flask import flash, redirect, render_template, url_for, request
import pdb


@app.route('/report', methods=('GET', 'POST'))
def get_report():

    if request.method == 'GET':
        return render_template('/reports/query.html')

    start_date = datetime.strptime(request.form['start_date'], '%m/%d/%Y')
    end_date = datetime.strptime(request.form['end_date'], '%m/%d/%Y')
    
    ''' I have to do this in two steps until I learn the right way'''
    invoice_query = [{'$match': {'paid_date': {'$gte': start_date, '$lte': end_date}}},
                    {'$sort': {'paid_date': 1}}
                    ]

    pipeline2 = [{'$match':  {'paid_date': {'$gte': start_date, '$lt': end_date }}} , 
                 {'$group':    {'_id': 'null',  'Amount': { '$sum': '$amount' },  'Hours': { '$sum': '$hours' } } } 
                ]

    invoices = db.invoice.aggregate(invoice_query)
    totals = db.invoice.aggregate(pipeline2).next()
    return render_template('/reports/results.html', items=invoices, totals=totals)
