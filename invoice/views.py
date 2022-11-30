from .. import app, client, db, next_sequence
from flask import flash, redirect, render_template, url_for, session, request, make_response
import pdb
from timesheet.model import TimeSheet
from pymongo import DESCENDING
from bson import ObjectId
from datetime import datetime
import pdfkit

def recalc(invoice):
    invoice['hours'] = 0
    invoice['amount'] = 0
    for ts in invoice['detail']:
        rate_id = db.clients.find_one({'_id': invoice['client']})['rate']
        invoice['hours'] += float(ts['hours'])
        invoice['rate'] = db.rates.find_one({'_id': int(rate_id)})['rate']
    
    invoice['amount'] = float(invoice['hours'] * invoice['rate'])
    return invoice
     

@app.route('/')
@app.route('/invoice_list', methods=('GET', 'POST'))
def invoice_list():
    page_number = 1
    filter = {}
    if request.args.get('page_number'):
        page_number = int(request.args.get('page_number'))
    if request.args.get('client_id'):
        client_id = request.args.get('client_id')
        filter = {'client': int(client_id)}

    invoice_count = db.invoice.count_documents(filter)
    clients = db.clients.find()
    
    clist = {}
    for client in clients:
        clist[client['_id']] = client['name']
        
    page_size = 20
    page_count = int(invoice_count / page_size)
    
    items = db.invoice.find(filter).skip(
        (page_number - 1) * page_size).limit(page_size).sort('date', DESCENDING)
    return render_template('/invoice/list.html', items=items, clients=clist,
                           item_count=invoice_count, page_number=page_number, 
                           page_size=page_size, page_count=page_count)


@app.route('/invoice_post/<int:invoice_id>', methods=('GET', 'POST'))
def invoice_post(invoice_id):
    '''Mark this invoice as paid and enter a check id'''
    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))

    invoice = db.invoice.find_one({'_id': invoice_id})

    if request.method == 'GET':
        return render_template('invoice/post.html', invoice=invoice)

    if 'sent' in request.form:
        db.invoice.update_one({'_id': invoice_id}, {'$set': {'sent': 'Y'}})
        return redirect(url_for('invoice_list'))

    if request.form['check_number'] == '' or request.form['date'] == '':
        if request.form['date'] == '':
            flash('Received date is required', category='error')
        else:
            invoice['paid_date'] = datetime.strptime(
                request.form['date'], '%m/%d/%Y')
        if request.form['check_number'] == '':
            flash('Check number is required', category='error')
        else:
            invoice['check_number'] = request.form['check_number']
        return render_template('invoice/post.html', invoice_id=invoice_id, invoice=invoice)

    db.invoice.update_one({'_id': invoice_id},{'$set': 
        {'check_number': request.form['check_number'],
         'status': 'paid',
         'paid_date': datetime.strptime(request.form['date'], '%m/%d/%Y')
         }
        }
        )
                           
    return redirect(url_for('invoice_list'))


@app.route('/invoice_close/<int:invoice_id>', methods=('GET', 'POST'))
def invoice_close(invoice_id):

    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))

    if request.method == 'GET':
        invoice = db.invoice.find_one({'_id': invoice_id})
        if invoice['close_date'] == '':
            invoice['close_date'] = datetime.now()
        return render_template('invoice/close.html', invoice=invoice)

    close_date = datetime.strptime(request.form['date'], '%m/%d/%Y')
    db.invoice.update_one({'_id': invoice_id}, {'$set': 
                          {'status': 'closed','close_date': close_date}})
    return redirect(url_for('invoice_list'))


@app.route('/invoice_open/<int:invoice_id>', methods=['GET'])
def invoice_open(invoice_id):
    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))

    kv = {'status': 'open', 'close_date': ''}
    db.invoice.update_one({'_id': invoice_id}, {'$set': kv})
    return redirect(url_for('invoice_edit', invoice_id=invoice_id))


@app.route('/invoice_delete/<int:invoice_id>')
def invoice_delete(invoice_id):
    return "Delete invoice"


@app.route('/invoice_edit/<int:invoice_id>')
def invoice_edit(invoice_id):
    """
    Reads back the invoice and sorts the detail by date
    """
    invoice = db.invoice.find_one({'_id': invoice_id})
    invoice['detail'] = sorted(invoice['detail'], key = lambda k: k['date'])
    return render_template('/invoice/edit.html', invoice=invoice)


@app.route('/invoice_create', methods=('GET', 'POST'))
def invoice_create():
    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))

    clients = db.clients.find()
    if request.method == 'GET':
        return render_template('invoice/create.html', clients=clients)

    invoice = {}
    client_id = int(request.form['client_id'])
    client_rec = db.clients.find_one({'_id': client_id})
    rate = db.rates.find_one(int(client_rec['rate']))

    invoice['_id'] = next_sequence('invoice')
    invoice['date'] = datetime.strptime(request.form['date'], '%m/%d/%Y')
    invoice['hours'] = float(0)
    invoice['client'] = client_id
    invoice['amount'] = float(0)
    invoice['detail'] = []
    invoice['status'] = 'open'
    invoice['check_number'] = ''
    invoice['period'] = next_sequence('period')
    invoice['close_date'] = ''
    invoice['posted'] = False
    invoice['sent'] = ''
    invoice['rate'] = rate['rate']
    
    db.invoice.insert_one(invoice)
    return redirect(url_for('invoice_list'))


@app.route('/invoice_view/<int:invoice_id>', methods=['GET'])
def invoice_view(invoice_id):
    import pdb
    
    today = datetime.now().strftime('%m/%d/%Y')
    invoice = db.invoice.find_one({'_id': invoice_id})
    client_rec = db.clients.find_one({'_id': invoice['client']})
    company = db.company.find_one({'_id': 1})
    rate = db.rates.find_one({'_id': int(client_rec['rate'])})
    invoice['rate'] = rate['rate']

    action = request.args['action']

    args = {}
    args['invoice'] = invoice
    args['client'] = client_rec
    args['date'] = today
    args['action'] = action
    args['company'] = company

    if action == 'print':
        if invoice['status'] == 'open':
            flash('Invoice must first be closed')
            return render_template('invoice/view.html', 
                                   invoice=invoice, date=today, company=company, 
                                   client=client_rec, action='view')
        options = {
            'page-size': 'Letter',
            'margin-left': '0.75in',
            'margin-right': '0.75in',
            'margin-top': '0.75in',
            'margin-bottom': '0.75in'
        }

        inv_date = invoice['date'].strftime('%Y%m%d')
        invoice['rate'] = rate['rate']

        if 'close_date' in invoice:
            if invoice['close_date']:
                inv_date = invoice['close_date'].strftime('%Y%m%d')
                
        if len(invoice['detail']) > 0:
            invoice['detail'] = sorted(invoice['detail'], key = lambda k: k['date'])

        file_name = '{}-{}-{}.pdf'.format(client_rec['prefix'], inv_date, str(invoice['_id']))
        _invoice = render_template('invoice/view.html', invoice=invoice,
                                   date=today, company=company, client=client_rec, action=action)
        _sheet = pdfkit.from_string(_invoice, False, options=options)
        response = make_response(_sheet)
        response.headers['Content-type'] = 'application/pdf'
        response.headers['Content-disposition'] = 'inline; filename='+file_name
        return response

    return render_template('invoice/view.html', invoice=invoice, date=today, company=company, client=client_rec, action=action)
