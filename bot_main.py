import json
import os


class Checker:
    def __init__(self, std):
        self.std = std

    def __new__(cls, std):
        def __check():
            self = std
            print(self.data)
            try:
                if self.data['Login'] == self.logpass[0]:
                    if self.data['Passwd'] == self.logpass[1]:
                        print('Access granted')
                        return True
                    else:
                        print('Invalid passwd')
                        return False
                else:
                    print('Invalid login')
                    return False
            except TypeError:
                print('Користувача не знайдено.')

        if __check():
            return std
        else:
            return None


class Archive:
    def __init__(self, fname, lname, clsname):
        self.fname = fname
        self.lname = lname
        self.clsname = clsname

        self.isArchive = True
        if 'data.json' in os.listdir():
            self.data = self.__readjson()

        else:
            self.__createjson()

    def getData(self):
        return self.data[self.clsname][f'{self.fname} {self.lname}']

    def writejson(self, data):
        with open('data.json', 'w') as file:
            json.dump(data, file)

    def __createjson(self):
        open('data.json', 'w')

    def __readjson(self):
        with open('data.json', 'r') as file:

            json_r = json.load(file)
            if not json_r:
                self.isArchive = False
                print('Json is empty')
                return
            else:
                data = json_r
                print(data)
        return data


class Person:
    def __init__(self, fname, lname, ):
        self.fname = fname
        self.lname = lname
        self.logpass = self.__login()
        self.archive = Archive(fname, lname, self.__class__.__name__)
        self.data = self.archive.getData()

    # def saveChanges(self):
    #     self.archive.writejson()

    def __login(self):
        log = input('Введіть логін: ')
        passwd = input('Введіть пароль: ')
        return log, passwd


class Students(Person):
    def __init__(self, firstname, lastname):
        Person.__init__(self, firstname, lastname)

    def WatchMarks(self):
        for k, v in self.data['Marks'].items():
            print(f'{k}: {v}')


std = Checker(Students('Orlov', 'Volodya'))
std.WatchMarks()

"""
std = Checker(Students('Orlov', 'Volodya')) //None or Student
"""
