from .. import app, db, next_sequence
from flask import redirect, render_template, url_for, session, request
import pdb
from pymongo import ASCENDING
from contractor.site.form import ContactForm

def get_rates():
    rates = {}
    for r in db.rates.find():
        rates[str(int(r['_id']))] = int(r['rate'])
    return rates

def get_states():
    states = db.control.find_one({'_id': 'states'})
    _ = states.pop('_id')
    return states

@app.route('/company_list')
def company_list():
    items = db.company.find().sort('name', ASCENDING)
    return render_template('site/company_list.html', items=items)

@app.route('/company_create', methods=("GET", "POST"))
def company_create():
    if 'cancel' in request.form:
        return redirect(url_for('company_list'))

    if 'delete' in request.form:
        db.company.delete_one({'_id': int(request.form['id'])})
        return redirect(url_for('company_list'))
    
    company = {}
    
    if request.method == 'GET':
        return render_template('site/company.html',company=company,action='create',states=get_states())
    
    company['name'] = request.form['name']
    company['address1'] = request.form['address1']
    company['address2'] = request.form['address2']
    company['city'] = request.form['city']
    company['state'] = request.form['states']
    company['zip'] = request.form['zip']
    company['attn'] = request.form['attn']
    company['phone'] = request.form['phone']
    company['email'] = request.form['email']

    if request.form['action'] == 'create':
        company['_id'] = next_sequence('company')    
        db.company.insert_one(company)
    else:
        db.company.update_one({'_id': int(request.form['id'])}, {'$set': company})

    return redirect(url_for('company_list'))

@app.route('/company_edit/<int:company_id>', methods=("GET", "POST"))
def company_edit(company_id):

    if request.method == 'GET':
        company = db.company.find_one({'_id': company_id})
        return render_template('site/company.html',company=company,action='edit',states=get_states())
    company = {}
    company['_id'] = company_id
    company['name'] = request.form['name']
    company['address1'] = request.form['address1']
    company['address2'] = request.form['address2']
    company['city'] = request.form['city']
    company['state'] = request.form['states']
    company['zip'] = request.form['zip']
    company['attn'] = request.form['attn']
    company['phone'] = request.form['phone']
    company['email'] = request.form['email']
    db.company.update_one({'$set': company})
    return redirect(url_for('company_list'))

@app.route('/client_create', methods=['POST'])
def client_create():
    form = ContactForm()
    form.client_id = -1
    cust = {'_id': -1}
    return render_template('/site/contact.html', headline='Client Info',client=cust,rates=get_rates(),states=get_states(),action='create')

@app.route('/client_edit/<client_id>', methods=('GET', 'POST'))
@app.route('/client_edit/<int:client_id>', methods=('GET', 'POST'))
def client_edit(client_id=None):

    if 'cancel' in request.form:
        return redirect(url_for('client_list'))

    client_id = int(client_id)
    
    if 'delete' in request.form:
        db.clients.delete_one({'_id': client_id})
        return redirect(url_for('client_list'))

    if request.method == 'GET':
        if client_id != -1:
            cust = db.clients.find_one({'_id': client_id})
            return render_template('/site/contact.html', headline='Client Info',client=cust,rates=get_rates(),states=get_states(),action='edit')    

    is_new = False
    if client_id == -1:
        is_new = True
        client_id = next_sequence('client')

    cust = {}
    
    cust['_id'] = client_id
    cust['name'] = request.form['name']
    cust['address1'] = request.form['address1']
    cust['address2'] = request.form['address2']
    cust['city'] = request.form['city']
    cust['state'] = request.form['states']
    cust['zip'] = request.form['zip_code']
    cust['attn'] = request.form['attn']
    cust['phone'] = request.form['phone']
    cust['email'] = request.form['email']
    cust['rate'] = request.form['rate']
    cust['prefix'] = request.form['prefix']
    cust['fax'] = request.form['fax']
    cust['timesheet_form'] = request.form['timesheet_form']
    cust['project'] = request.form['project']

    if is_new:
        db.clients.insert_one(cust)
    else:
        db.clients.update_one({'_id': client_id}, {'$set': cust})

    return redirect(url_for('client_list'))

@app.route('/client_view/<int:client_id>', methods=['GET'])
def client_view(client_id):
    form = ContactForm()
    cl = db.clients.find_one({'_id': client_id})
    form['client_id'] = client_id
    form['cname'] = cl.name
    form['address1'] = cl.address1
    form['address2'] = cl.address2
    form['city'] = cl.city
    form['state'] = cl.state
    form['zip_code'] = cl.zip
    form['phone'] = cl.phone
    form['email'] = cl.email
    form['attn'] = cl.attn
    form['prefix'] = cl.prefix
    form['fax'] = cl.fax
    form['timesheet_form'] = cl.timesheet_form
    form['project'] = cl.project
    return render_template('site/client_view.html', headline="Client View", form=form)

@app.route('/client_list')
def client_list():
    clients = db.clients.find().sort('name', ASCENDING)
    return render_template('/site/client_list.html', items=clients)

@app.route('/control', methods=('GET', 'POST'))
def control_edit():
    items = db.control.find({'_id': {'$ne': 'states'}})
    
    if request.method =='GET':
        return render_template('/site/control.html',headline='Control',items=items)

    if 'cancel' in request.form:
        return redirect(url_for('invoice_list'))
    
    db.control.update_one( {'_id': 'client'}, { '$set': {'seq': int(request.form['client'])} } )
    db.control.update_one( {'_id': 'company'}, { '$set': {'seq': int(request.form['company'])} } )
    db.control.update_one( {'_id': 'invoice'}, { '$set': {'seq': int(request.form['invoice'])} } )
    db.control.update_one( {'_id': 'timesheet'}, { '$set': {'seq': int(request.form['timesheet'])} } )

    return render_template('/site/control.html',headline='Control',items=items)
