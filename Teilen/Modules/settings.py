import json

class Setting:
    def __init__(self):
        self.secret_key = ""
        self.data_bases={}

        self.data = self.load_json()

    def load_json(self):
        return json.load(open('env.json'))

    def get_secret_key(self):
        self.secret_key = self.data['secret_key']

        return self.secret_key

    def get_data_base(self):
        self.data_bases = {
            'default': {
                'ENGINE': self.data['db']['ENGINE'],
                'NAME': self.data['db']['NAME'],
                'USER': self.data['db']['USER'],
                'PASSWORD': self.data['db']['PASSWORD'],
                'HOST': self.data['db']['HOST'],
                'PORT': self.data['db']['PORT'],
            }
        }

        return self.data_bases

    def get_host_email_user(self):
        self.email_host = self.data['email_host']

        return self.email_host

    def get_from_email(self):
        self.from_email = self.data['from_email']

        return self.from_email

    def get_email_password(self):
        self.email_password = self.data['email_password']

        return self.email_password
