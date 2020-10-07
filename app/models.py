from datetime import datetime

class Tweet():
    def __init__(self, text):
        self.text = text
        self.id = None
        self.created_at = datetime.now()
