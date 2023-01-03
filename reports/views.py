from .. import app, client, db
from datetime import datetime
from flask import flash, redirect, render_template, url_for, request, make_response
import pdfkit
import pdb
import os


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
    
    invoices = [i for i in db.invoice.aggregate(invoice_query)]
    
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


@app.route('/timesheet/<int:invoice_id>', methods=['GET'])
def view_timesheet(invoice_id):

        company_rec = db.company.find_one({'_id': 1})
        invoice_rec = db.invoice.find_one({'_id': invoice_id})
        
        
        invoice_rec['detail'] = sorted(invoice_rec['detail'], key = lambda k: k['date'])
        
        inv_date = datetime.strftime(invoice_rec['date'], '%m%d%Y')
        start_date = datetime.strftime(invoice_rec['date'], '%m/%d/%Y')
        file_name_end_date = datetime.strftime(invoice_rec['close_date'], '%m%d%Y')
        end_date = datetime.strftime(invoice_rec['close_date'], '%m/%d/%Y')
        
        invoice_rec['date'] = start_date
        invoice_rec['close_date'] = end_date
                
        client_rec = db.clients.find_one({'_id': invoice_rec['client']})
        
        form_name = client_rec['timesheet_form']
        
        action = request.args['action']
        
        # convert the detail dates to a string and format hours to 2 decimal places
        for day,detail in enumerate(invoice_rec['detail']):
            work_date = datetime.strftime(invoice_rec['detail'][day]['date'],'%m/%d/%Y')
            invoice_rec['detail'][day]['date'] = work_date
            
            dd = float(invoice_rec['detail'][day]['hours'])
            
            if invoice_rec['detail'][day]['hours']:
                try:
                    hrs = "{:.2f}".format(dd)
                except:
                    pdb.set_trace()

                invoice_rec['detail'][day]['hours'] = hrs
            invoice_rec['detail'][day]['task'] = 'Conversion'
                
        # pad the detail out to 14 days 
        for day in range(len(invoice_rec['detail']), 14):
            invoice_rec['detail'].append({'date': '', 'description': '', 'hours': '', 'task': ''})
            
        
        if action=='view':
            return render_template('reports/'+form_name,invoice=invoice_rec,action='view')
    
        options = {
            'page-size': 'Letter',
            'margin-left': '0.75in',
            'margin-right': '0.75in',
            'margin-top': '0.75in',
            'margin-bottom': '0.75in'
        }
        
        entity_name = company_rec['attn'].replace(' ','_')
        
        file_name = '{}_Timesheet_{}.pdf'.format(entity_name, file_name_end_date)
        css_name = form_name.partition('.')[0]+'.css'
        css_path = os.path.dirname(os.path.abspath(__file__)) + '/../templates/reports/'+css_name
        _invoice = render_template('/reports/'+form_name, invoice=invoice_rec, action='print')
                                   
        _sheet = pdfkit.from_string(_invoice, False, css=css_path, options=options)
        response = make_response(_sheet)
        response.headers['Content-type'] = 'application/pdf'
        response.headers['Content-disposition'] = 'inline; filename='+file_name
        return response
        