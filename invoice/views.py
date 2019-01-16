from contractor import app, client, db, next_sequence
from flask import redirect, render_template, url_for, session, request
import pdb
from timesheet.model import TimeSheet
from pymongo import DESCENDING
from bson import ObjectId
from datetime import datetime

@app.route('/')
@app.route('/invoice_list')
def invoice_list():
    items = db.invoice.find().sort('date', DESCENDING)
    return render_template('/invoice/list.html', items=items)

@app.route('/invoice_close/<int:invoice_id>', methods=('GET', 'POST'))
def invoice_close(invoice_id):
    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))

    if request.method == 'GET':
        invoice = db.invoice.find_one({'_id': invoice_id})
        return render_template('invoice/close.html', invoice = invoice)

    if request.form['receipt_id'] == "":
        return redirect(request.referrer)

    invoice = db.invoice.find_one({'_id': invoice_id})
    invoice['check_number'] = request.form['receipt_id']
    invoice['status'] = 'closed'
    invoice['closed_date'] = datetime.now()
    db.invoice.update({'_id': invoice_id}, invoice)
    return redirect(url_for('invoice_list'))

@app.route('/invoice_delete/<int:invoice_id>')
def invoice_delete(invoice_id):
    return "Delete invoice"
    
@app.route('/invoice_edit/<int:invoice_id>')
def invoice_edit(invoice_id):
    invoice = db.invoice.find_one({'_id': invoice_id})
    return render_template('/invoice/edit.html', invoice=invoice)

@app.route('/invoice_create', methods=('GET', 'POST'))
def invoice_create():
    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))
    
    if request.method == 'GET':
        return render_template('invoice/create.html')
    
    invoice = {}
    
    invoice['_id'] = next_sequence('invoice')
    invoice['date'] = request.form['date']
    invoice['hours'] = 0
    invoice['amount'] = 0
    invoice['detail'] = []
    invoice['status'] = 'open'
    invoice['check_number'] = ''
    invoice['period'] = next_sequence('period')
    invoice['closed_date'] = ''
    invoice['posted'] = False
    db.invoice.insert_one(invoice)
    return redirect(url_for('invoice_list'))
    