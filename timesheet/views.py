import pdb

from bson import ObjectId
from datetime import datetime
from flask import redirect, render_template, request, session, url_for
from pymongo import ASCENDING, DESCENDING
from contractor import app, client, db, next_sequence
from timesheet.model import TimeSheet

@app.route('/timesheet')
def timesheet_list():
    ts = db.timesheet
    list = ts.find({}).sort('date', DESCENDING)
    return render_template('timesheet/list.html', items=list)

@app.route('/delete/<int:tsid>', methods=['GET'])
def timesheet_delete(tsid):
    if tsid:
        db.timesheet.delete_one({'_id': ObjectId(tsid)})
    return redirect(url_for('timesheet_list'))

@app.route('/timesheet_entry/<int:invoice_id>')
def timesheet_entry(invoice_id):
    return render_template('timesheet/entry.html', invoice_id=invoice_id)

@app.route('/timesheet_edit/<int:inv_id>/<int:tsid>', methods=('GET', 'POST'))
def timesheet_edit(inv_id, tsid):
    
    if 'cancel_button' in request.form:
        return redirect( url_for('invoice_edit',invoice_id=inv_id))

    invoice = db.invoice.find_one({'_id': inv_id})
    ts = None
    ts_index = -1
    for ts in invoice['detail']:
        ts_index += 1
        if tsid == ts['_id']:
            break
    if ts is None:
        return redirect( url_for('invoice_edit',invoice_id=inv_id))

    if request.method == 'GET':
        return render_template('timesheet/edit.html',invoice_id=inv_id,item=ts)
    ts['date'] = datetime.strptime(request.form['date'],'%m/%d/%Y')
    ts['description'] = request.form['description']
    ts['hours'] = request.form['hours']

    invoice['detail'][ts_index] = ts

    db.invoice.replace_one({'_id': inv_id}, invoice, True)

    return redirect(url_for('invoice_edit',invoice_id=inv_id))

@app.route('/timesheet_create/<int:invoice_id>', methods=('GET', 'POST'))
def timesheet_create(invoice_id):
    if 'submit_button' in request.form:
        
        entry = {}
        if not request.form['date']:
            return render_template(url_for('entry'))
        if not request.form['description']:
            return render_template(url_for('entry'))
        if not request.form['hours']:
            return render_template(url_for('entry'))

        entry['_id'] = next_sequence('timesheet')
        entry['date'] = datetime.strptime(request.form['date'],'%M/%d/%Y')
        entry['description'] = request.form['description']
        entry['hours'] = int(request.form['hours'])
        db.timesheet.insert_one(entry)

        invoice = db.invoice.find_one({'_id': invoice_id})
        invoice['hours'] += entry['hours']
        invoice['amount'] = invoice['hours'] * 50
        db.invoice.replace_one({'_id': invoice_id}, invoice, True)

        db.invoice.update({'_id': invoice_id}, { '$push': {'detail': entry}})

    return redirect(url_for('invoice_edit',invoice_id=invoice_id))
