from contractor import app, client, db, next_sequence
from flask import redirect, render_template, url_for, session, request, make_response
import pdb
from timesheet.model import TimeSheet
from pymongo import DESCENDING
from bson import ObjectId
from datetime import datetime
import pdfkit

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
        return redirect(url_for('invoice_list'))

    invoice = db.invoice.find_one({'_id': invoice_id})
    invoice['check_number'] = request.form['receipt_id']
    invoice['status'] = 'closed'
    invoice['closed_date'] = datetime.now()
    db.invoice.update({'_id': invoice_id}, invoice)
    return redirect(url_for('invoice_list'))

@app.route('/invoice_post/<int:invoice_id>', methods=['GET'])
def invoice_post(invoice_id):
    invoice = db.invoice.find_one({'_id': invoice_id})
    invoice['status'] = 'posted' 
    db.invoice.update({'_id': invoice_id}, invoice)
    return redirect(url_for('invoice_list'))       

@app.route('/invoice_open/<int:invoice_id>', methods=['GET'])
def invoice_open(invoice_id):
    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))

    invoice = db.invoice.find_one({'_id': invoice_id})
    invoice['check_number'] = ''
    invoice['status'] = 'open'
    invoice['closed_date'] = ''
    db.invoice.update({'_id': invoice_id}, invoice)
    return redirect(url_for('invoice_edit',invoice_id=invoice_id))

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
    invoice['date'] = datetime.strptime(request.form['date'], '%m/%d/%Y')
    invoice['hours'] = 0
    invoice['client'] = request.form['client_id']
    invoice['amount'] = float(0)
    invoice['detail'] = []
    invoice['status'] = 'open'
    invoice['check_number'] = ''
    invoice['period'] = next_sequence('period')
    invoice['closed_date'] = ''
    invoice['posted'] = False
    db.invoice.insert_one(invoice)
    return redirect(url_for('invoice_list'))

@app.route('/invoice_view/<int:invoice_id>', methods=['GET'])
def invoice_view(invoice_id):

    today = datetime.now().strftime('%m/%d/%Y')
    invoice = db.invoice.find_one({'_id': invoice_id})
    client_rec = db.clients.find_one({'_id': invoice['client']})
    company = db.company.find_one({'_id': 1})

    action = request.args['action']

    args = {}
    args['invoice'] = invoice
    args['client'] = client_rec
    args['date'] = today
    args['action'] = action
    args['company'] = company

    if action == 'print':
        options = {
            'page-size': 'Letter',
            'margin-left': '0.75in',
            'margin-right': '0.75in',
            'margin-top': '0.75in',
            'margin-bottom': '0.75in'
        }
        _invoice = render_template('invoice/view.html',invoice=invoice,date=today,company=company,client=client_rec,action=action)
        _sheet = pdfkit.from_string(_invoice, False, options=options)
        response = make_response(_sheet)
        response.headers['Content-type'] = 'application/pdf'
        response.headers['Content-disposition'] = 'inline; filename=output.pdf'
        return response
    
    return render_template('invoice/view.html',invoice=invoice,date=today,company=company,client=client_rec,action=action)
