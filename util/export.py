import mvsupport as mvs
import qmclient as qm
from pymongo import MongoClient, DESCENDING, ASCENDING
import pdb

qm_connection = None
db = None

def mongo_connect():
    global db
    if db is None:
        mongo_client = MongoClient('127.0.0.1', 27017)
        db = mongo_client['contractor']
        
    
def qm_connect():
    global qm_connection
    if qm_connection is None:
        qm_connection = qm.ConnectLocal("QMUSERS")
        if qm_connection != 1:
            print("Cannot connect to server {}".format(qm.Error()))
            raise Exception

def export_invoice():
    """
    1              D      1                         CLIENT         3R       S
    2              D      2                         OPEN DATE      5R       S
    3              D      3                         HOURS          3R       S
    4              D      4                         TOTAL AMT      6R       S
    5              D      5                         CLOSE DATE     5R       S
    6              D      6                         SENT           1L       S
    7              D      7                         POSTED         1R       S
    8              D      8                         CHECK ID       10L      S
    9              D      9                         RATE           5R       S
    10             D      10                        TIMESHEETS     3R       M
    """
    invoice_file = qm.Open('INVOICE')
    
    invoices = db.invoice.find().sort('date', ASCENDING)
    for invoice in invoices:
        invoice_rec = ''
        invoice_date = qm.IConv(invoice['date'].strftime('%m/%d/%Y'),'D2MDY')
        if invoice['close_date'] != "":
            close_date = qm.IConv(invoice['close_date'].strftime('%m/%d/%Y'),'D2MDY')
        else:
            close_date = ''
        amt = str(invoice['amount'])
        if 'posted' not in invoice:
            posted = 'Y'
        else:
            posted = str(invoice['posted'])
        if 'check_id' not in invoice:
            check_id = ''
        else:
            check_id = str(invoice['check_id'])
        if 'rate' not in invoice:
            rate = '5000'
        else:
            rate = qm.IConv(str(invoice['rate']),'MR2')
        invoice_rec = qm.Replace(invoice_rec,1,0,0,str(invoice['client']))
        invoice_rec = qm.Replace(invoice_rec,2,0,0,invoice_date)
        invoice_rec = qm.Replace(invoice_rec,3,0,0,str(invoice['hours']))
        invoice_rec = qm.Replace(invoice_rec,4,0,0,qm.IConv(amt,'MR2'))
        invoice_rec = qm.Replace(invoice_rec,5,0,0,close_date)
        invoice_rec = qm.Replace(invoice_rec,6,0,0,str(invoice['sent']))
        invoice_rec = qm.Replace(invoice_rec,7,0,0,posted)
        invoice_rec = qm.Replace(invoice_rec,8,0,0,check_id)
        invoice_rec = qm.Replace(invoice_rec,9,0,0,rate)
        for idx,val in enumerate(invoice['detail']):
            invoice_rec = qm.Replace(invoice_rec,10,idx+1,0,str(val['_id']))
        invoice_id = str(invoice['_id'])
        qm.Write(invoice_file, invoice_id, invoice_rec)
        
def export_timesheet():
    """
    1              D      1                         DATE           5L       S
    2              D      2                         WORK DONE      100L     S
    3              D      3                         HOURS          10L      S
    4              D      4                         INVOICE        5R       S
    """
    timesheet_file = qm.Open("TIMESHEET")
    invoices = db.invoice.find().sort('date', ASCENDING)
    for invoice in invoices:
        if 'detail' not in invoice:
            continue
        for timesheet in invoice['detail']:
            timesheet_rec = ''
            if 'date' not in timesheet or timesheet['date'] == '':
                continue
            ts_date = qm.IConv(timesheet['date'].strftime('%m/%d/%Y'),'D2MDY')
            ts_desc = timesheet['description']
            ts_hours = str(timesheet['hours'])
            ts_id = str(timesheet['_id'])
            ts_invoice_id = str(invoice['_id'])
            timesheet_rec = qm.Replace(timesheet_rec,1,0,0,ts_date)
            timesheet_rec = qm.Replace(timesheet_rec,2,0,0,ts_desc)
            timesheet_rec = qm.Replace(timesheet_rec,3,0,0,ts_hours)
            timesheet_rec = qm.Replace(timesheet_rec,4,0,0,ts_invoice_id)
            qm.Write(timesheet_file, ts_id, timesheet_rec)


if __name__ == '__main__':
    qm_connect()
    mongo_connect()
    #export_invoice()
    export_timesheet()
    qm.Disconnect()    
