from contractor import app, client, db, next_sequence
from flask import redirect, render_template, url_for, session, request
import pdb
from pymongo import ASCENDING

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
