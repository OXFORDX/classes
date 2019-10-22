import pydatabase
import sqlite3
import xlsxwriter


class Stude:
    def __init__(self, fname, lname):
        self.data = pydatabase.Database(f'{fname} {lname}')
        self.fname = fname
        self.lname = lname

    def WatchMarks(self):
        return self.data.excelDBwrite()

    def GetCertificate(self):
        with open('Certificates/dov2.jpg', 'rb') as foto:
            return foto


class Teacher:
    def __init__(self, flname):
        rand = flname.split(' ')
        self.fname = rand[0]
        self.lname = rand[1]
        self.data = pydatabase.Database()
        self.connection = sqlite3.connect("Database/teachers.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT subject FROM teachers WHERE firstname=:firstname AND lastname=:lastname", {
                'firstname': self.fname,
                'lastname': self.lname
            })
        self.subject = self.cursor.fetchone()['subject']

    def changeMarks(self, group):
        print(self.data.excelDBwrite(group, self.subject))


class Dean:
    def __init__(self):
        db = pydatabase.Database()


x = Dean()