import json
import os

root = os.getcwd()


class Session:
    def __init__(self, id):
        self.id = id
        self.data = {}
        if f'{id}.json' in os.listdir('temp/Sessions'):
            self.data = self.readstate()
            print(self.data['prev_msg'])
        else:
            self.createuser()

    def createuser(self):
        if 'Sessions' not in os.listdir('temp'):
            os.mkdir('temp/Sessions')
        self.data = {
            'name': '',
            'id': self.id,
            'state': None,
            'prev_msg': '/start'
        }
        with open(f'temp/Sessions/{self.id}.json', 'w') as js:
            json.dump(self.data, js, indent=2)

    def readstate(self):
        with open(f'temp/Sessions/{self.id}.json', 'r') as js:
            return json.loads(js.read())

    def writestate(self, state):
        self.data['state'] = state

    def writemess(self, mess):
        self.data['prev_msg'] = mess

    def writename(self, name):
        self.data['name'] = name

    def close(self):
        with open(f'temp/Sessions/{self.id}.json', 'w') as js:
            json.dump(self.data, js, indent=2)


if __name__ == '__main__':
    x = Session('123456')
    x.writestate(3)
    x.writemess('Blya')
    x.close()
