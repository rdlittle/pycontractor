from db import DB
from datetime import datetime as dt
import qmclient as qm
import mvsupport as mvs

connection = None

class QM(DB):

    def __init__(self, *args, account='QMUSERS',**kwargs):
        global connection
        if connection is None:
            connection = qm.ConnectLocal(account)
            if connection != 1:
                print("Cannot connect to server {}".format(qm.Error()))
                raise Exception
            
    def query(self, *args, **kwargs):
        super().query(*args, **kwargs)
        file_name = kwargs['file']
        start_date = '1'
        end_date = self.today()
        if 'start_date' in kwargs:
            start_date = qm.IConv(kwargs['start_date'],'D')
        if 'end_date' in kwargs:
            end_date = qm.IConv(dt.strftime(
                kwargs['end_date'],'%m/%d/%Y'),'D')
            
    def invoice_list(self,*args, **kwargs):
        if 'start_date' in kwargs:
            start_date = qm.IConv(kwargs['start_date'],'D')
        if 'end_date' in kwargs:
            end_date = qm.IConv(dt.strftime(
                kwargs['end_date'],'%m/%d/%Y'),'D')
        
            
        
    def today(self):
        return qm.IConv(dt.strftime(dt.now(),'%m/%d/%Y'),'D')
    