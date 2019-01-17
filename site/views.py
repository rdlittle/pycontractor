from contractor import app, db, next_sequence
from flask import redirect, render_template, url_for, session, request
import pdb
from pymongo import ASCENDING
from contractor.site.form import ContactForm

@app.route('/company_list')
def company_list():
    items = db.company.find().sort('name', ASCENDING)
    return render_template('site/company_list.html', items=items)

@app.route('/company_create', methods=("GET", "POST"))
def company_create():
    if 'cancel' in request.form:
        return redirect(url_for('company_list'))
    
    company = {}
    if request.method == 'GET':
        return render_template('site/company.html',company=company,action='create')
    
    company['name'] = request.form['name']
    company['address1'] = request.form['address1']
    company['address2'] = request.form['address2']
    company['city'] = request.form['city']
    company['state'] = request.form['state']
    company['zip'] = request.form['zip']
    company['attn'] = request.form['attn']
    company['phone'] = request.form['phone']
    company['email'] = request.form['email']

    if 'create' in request.form:
        company['_id'] = next_sequence('company')    
        db.company.insert(company)
    else:
        db.company.update({'_id': request.form['id']}, company)

    return redirect(url_for('company_list'))

@app.route('/company_edit/<int:company_id>', methods=("GET", "POST"))
def company_edit(company_id):

    if request.method == 'GET':
        company = db.company.find_one({'_id': company_id})
        return render_template('site/company.html',company=company,action='edit')

    company = {}
    company['_id'] = company_id
    company['name'] = request.form['name']
    company['address1'] = request.form['address1']
    company['address2'] = request.form['address2']
    company['city'] = request.form['city']
    company['state'] = request.form['state']
    company['zip'] = request.form['zip']
    company['attn'] = request.form['attn']
    company['phone'] = request.form['phone']
    company['email'] = request.form['email']
    db.company.update(company)
    return redirect(url_for('company_list'))

@app.route('/client_create', methods=['POST'])
def client_create():
    form = ContactForm()
    form.client_id = -1
    return render_template('/site/contact.html', headline='Client Info', form=form)

@app.route('/client_edit/<client_id>', methods=('GET', 'POST'))
def client_edit(client_id=None):
    form = ContactForm()
    pdb.set_trace()
    if request.method == 'GET' and client_id != -1:
        cust = db.client.find_one({'_id': client_id})
        form.client_id = cust['_id']
        form.name = cust['name']
        form.address1 = cust['address1']
        form.address2 = cust['address2']
        form.city = cust['city']
        form.state = cust['state']
        form.zipCode = cust['zip']
        form.attn = cust['attn']
        form.phone = cust['phone']
        form.email = cust['email']
        render_template('/site/contact.html', headline='Client Info',form=form)    
    
    cust = {}
    cust['_id'] = form.client_id
    cust['name'] = form.name
    cust['address1'] = form.address1
    cust['address2'] = form.address2
    cust['city'] = form.city
    cust['state'] = form.state
    cust['zip'] = form.zipCode
    cust['attn'] = form.attn
    cust['phone'] = form.phone
    cust['email'] = form.email
    if client_id == -1:
        cust['_id'] = next_sequence('client')
        db.client.insert(cust)
        return "Client added"

    db.clients.update(cust)
    return "Client updated"

@app.route('/client_list')
def client_list():
    clients = db.clients.find().sort('name', ASCENDING)
    return render_template('/site/client_list.html', items=clients)
