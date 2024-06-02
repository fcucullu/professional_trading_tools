from datetime import datetime

class Token:
    def __init__(self, response):
        self.access = response['access_token']
        self.refresh = response['refresh_token']
        self.exp_date = datetime.strptime(response['.expires'], '%a, %d %b %Y %H:%M:%S %Z')

    def __str__(self):
        return self.access

    def is_valid(self):
        return self.access and self.exp_date > datetime.utcnow()

    def should_refresh(self):
        return not self.is_valid()