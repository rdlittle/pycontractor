from flask import Flask
from pymongo import MongoClient
import datetime

# print("contractor.__init__")
app = Flask(__name__)
app.config.from_object("settings")

client = MongoClient(app.config['DB_HOST'], app.config['DB_PORT'])
db = client[app.config['DATABASE']]

def next_sequence(coll):
    seq = int(db.control.find_one({'_id': coll})['seq'])
    db.control.update_one({'_id': coll}, {'$set': {'seq': seq + 1}})
    return seq

@app.template_filter()
def oconv_date(value, format='%m/%d/%Y'):
    if type(value) == datetime.datetime:
        return value.strftime(format)
    return datetime.datetime.fromisoformat(value).strftime(format)

@app.template_filter()
def iconv_date(value, format='%m/%d/%Y'):
    return datetime.datetime.strptime(value,format)

from contractor.timesheet import views
from contractor.invoice import views
from contractor.site import views