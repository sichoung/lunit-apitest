import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class APITestException(Exception):
    def __init__(self, message):
        self.value = message

    def __str__(self):
        return self.value
