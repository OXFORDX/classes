import sqlite3
import random
import pandas as pd
import os
from pandas import ExcelWriter
from pandas import ExcelFile

root = os.getcwd()
se

class Database:
    def __init__(self, flname):
        rand = flname.split(' ')
        self.fname = rand[0]
        self.lname = rand[1]
        self.connection = sqlite3.connect("Database/students.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        # cursor.execute("""CREATE TABLE students(
        #             id integer,
        #             firstname text,
        #             lastname text,
        #             age integer,
        #             faculty text,
        #             groups text,
        #             course integer,
        #             pay integer )""")
        #

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def addStd(self):
        self.cursor.execute(f"""CREATE TABLE std{self.__getLastID()}(
            subject text,
            mark integer)""")
        firstname = str(input('FName: '))
        lastname = str(input('LName: '))
        age = int(input('Age: '))
        faculty = str(input('Faculty: '))
        groups = str(input('Group: '))
        course = int(input('Course: '))
        pay = int(input('Pay: '))
        login = str(input('Login: '))
        passwd = str(input('Passwd: '))
        with self.connection:
            self.cursor.execute(
                "INSERT INTO students VALUES (:id, :firstname, :lastname, :age, :faculty, :groups, :course, :pay)",
                {
                    'id': self.__getLastID(),
                    'firstname': firstname,
                    'lastname': lastname,
                    'age': age,
                    'faculty': faculty,
                    'groups': groups,
                    'course': course,
                    'pay': pay
                })

    def addSubject(self, subject):
        with self.connection:
            self.cursor.execute(f"INSERT INTO std{self.getID()} VALUES (:subject, :mark)",
                                {'subject': subject, 'mark': 0})

    def changeMark(self, std, mark, subj):
        mark = int(mark)
        print(f'{std} {mark} {subj}')
        self.cursor.execute(f"UPDATE std{self.getID(std)} SET mark=:mark WHERE subject=:subject", {
            'mark': mark,
            'subject': subj
        })

    def getID(self, std=None):
        if not std:
            self.cursor.execute(f"""SELECT id FROM students WHERE firstname=:firstname AND lastname=:lastname""",
                                {'firstname': self.fname, 'lastname': self.lname})
            obj = self.cursor.fetchone()
            return obj['id']
        else:
            std = std.split(' ')
            fname = std[0]
            lname = std[1]
            self.cursor.execute(f"""SELECT id FROM students WHERE firstname=:firstname AND lastname=:lastname""",
                                {'firstname': fname, 'lastname': lname})
            obj = self.cursor.fetchone()
            return obj['id']

    def getGroupIDs(self, group):  # {1: std1, 2: std2, 3: std3}
        try:
            id_dict = {}
            self.cursor.execute(f"SELECT * FROM students WHERE groups=:groups", {'groups': group})
            obj = self.cursor.fetchall()
            for i in obj:
                id_dict[i['id']] = f"{i['firstname']} {i['lastname']}"
            print(id_dict)
            return id_dict
        except Exception as e:
            print('Invalid group')

    def excelDBwrite(self, group=None, subject=None):
        if group and subject:
            marks = []
            std = []
            for k, v in self.getGroupIDs(group).items():
                std.append(v)
                for j in self.cursor.execute(f"SELECT * FROM std{k} WHERE subject=:subj", {'subj': subject}):
                    marks.append(j['mark'])
            df = pd.DataFrame({'Студент': std, 'Оцінка': marks})
            df = df[['Студент', 'Оцінка']].sort_values(by='Студент')
            df.index = range(1, len(std) + 1)
            print(df)
            writer = pd.ExcelWriter(f'{subject}.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name=group)
            if group not in os.listdir('temp'):
                os.mkdir(f'temp/{group}')
            os.chdir(f'temp/{group}')
            writer.save()
            os.chdir(root)
        else:
            subj = []
            mark = []
            for i in self.cursor.execute(f"SELECT * FROM std{self.getID()}"):
                subj.append(i['subject'])
                mark.append(i['mark'])
            df = pd.DataFrame({'Предмет': subj, 'Оцінка': mark}, index=[i for i in range(1, len(mark) + 1)])
            return repr(df)

    def excelDBread(self, group, subject, filename):
        df = pd.read_excel(f'{subject}.xlsx', sheet_name=group)
        for i in df.index:
            self.changeMark(df['Студент'][i], df['Оцінка'][i], subject)

    def __readDB(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def __getLastID(self):
        last_id = 0
        for i in self.__readDB():
            last_id = i['id']
        return last_id + 1


def generateMarks(db, subj):
    for i in subj:
        db.changeMark(i, random.randint(60, 100))


def getNamesOfSTD():
    connection = sqlite3.connect("Database/students.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    std = []
    for i in cursor.execute(f"SELECT * FROM students"):
        std.append(f"{i['firstname']} {i['lastname']}")
    connection.close()
    return std


if __name__ == '__main__':
    # subjects = ['Математика', 'КПЗ', 'Психологія', 'Філософія', 'Веб-програмування']
    # db = Database('Ямковий Андрій')
    # # db.excelDB()
    # db.excelDBwrite('IP-82', 'КПЗ')
    # db.excelDBwrite()
    # print(getNamesOfSTD())
    # db.changeMark('Математика', 30)
    # # for i in subjects:
    # #    db.addSubject(i)
    # # generateMarks(db, subjects)
    # df = pd.DataFrame({'subjects': ['Математика', 'КПЗ', 'Психологія', 'Філософія', 'Веб-програмування'],
    #                    'marks': [90, 90, 90, 90, 90]})
    # print(df)
    # writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='Sheet1')
    # writer.save()
    conn = sqlite3.connect('')
