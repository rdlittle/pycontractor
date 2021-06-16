class Company(object):
    def __init__(self, *args, **kwargs):
        self.id = ''
        self.name = ''
        self.address1 = ''
        self.address2 = ''
        self.city = ''
        self.state = ''
        self.zip = ''
        self.attention = ''
        self.phone = ''
        self.email = ''
        
class Client(Company):
    def __init__(self, *args, **kwargs):
        super(Client,self).__init__(*args, **kwargs)
        self.rate = ''
