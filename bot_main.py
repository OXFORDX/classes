import json
import os


class Archive:
    def __init__(self, fname, lname, logpass):
        self.fname = fname
        self.lname = lname
        self.logpass = logpass
        if 'data.json' in os.listdir():
            self.data = self.__readjson()

        else:
            self.__createjson()
        if not self.__checker():
            self.__del__()

    def getData(self):
        return self.data[self.logpass[2]][f'{self.fname} {self.lname}']

    def __checker(self):
        try:
            if self.data[self.logpass[2]][f'{self.fname} {self.lname}'] \
                    and self.data[self.logpass[2]][f'{self.fname} {self.lname}']['Login'] == self.logpass[0]:
                if self.data[self.logpass[2]][f'{self.fname} {self.lname}']['Passwd'] == self.logpass[1]:
                    print('Access granted')
                    return True
                else:
                    print('Invalid passwd')
                    self.__del__()
                    return
            else:
                print('Invalid login')
                self.__del__()
                return
        except TypeError:
            print('Користувача не знайдено.')

    def writejson(self, data):
        with open('data.json', 'w') as file:
            json.dump(data, file)

    def __createjson(self):
        open('data.json', 'w')

    def __readjson(self):
        with open('data.json', 'r') as file:

            json_r = json.load(file)
            if not json_r:
                self.__del__()
                print('Json is empty')
                return
            else:
                data = json_r
                print(data)
        return data

    def __del__(self):
        print('Destructor')


class Person:
    def __init__(self, fname, lname, logpass):
        self.fname = fname
        self.lname = lname
        self.archive = Archive(fname, lname, logpass)
        self.data = self.archive.getData()

    def saveChanges(self):
        self.archive.writejson()


class Students(Person):
    def __init__(self, firstname, lastname):
        Person.__init__(self, firstname, lastname, self.__login())

    def __login(self):
        log = input('Введіть логін: ')
        passwd = input('Введіть пароль: ')
        return log, passwd, self.__class__.__name__

    def WatchMarks(self):
        for k, v in self.data['Marks'].items():
            print(f'{k}: {v}')


std = Students('Orlov', 'Volodya')
std.WatchMarks()
