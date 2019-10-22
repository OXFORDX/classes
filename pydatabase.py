import sqlite3
import random
import pandas as pd
import os
import xlsxwriter

root = os.getcwd()


class Database:
    def __init__(self, flname=None):
        if flname:
            rand = flname.split(' ')
            self.fname = rand[0]
            self.lname = rand[1]
        self.connection = sqlite3.connect("Database/students.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.subjects = ['Математика', 'КПЗ', 'Психологія', 'Філософія', 'Веб-програмування']

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
        df = pd.read_excel('temp/tempxlsx.xlsx', sheet_name='std')
        ara = []
        for i in df['Дані']:
            if type(i) is float:
                ara.append(None)
            else:
                ara.append(i)

        with self.connection:
            self.cursor.execute(f"""CREATE TABLE std{self.__getLastID()}(
                subject text,
                mark integer)""")
        id = self.__getLastID()
        with self.connection:
            self.cursor.execute(
                "INSERT INTO students VALUES (:id, :firstname, :lastname, :age, :faculty, :groups, :course, :pay)",
                {
                    'id': id,
                    'firstname': ara[0],
                    'lastname': ara[1],
                    'age': ara[2],
                    'faculty': ara[3],
                    'groups': ara[4],
                    'course': ara[5],
                    'pay': ara[6]
                })
        conn = sqlite3.connect('Database/passwd.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        with conn:
            cursor.execute("INSERT INTO passwd VALUES (:id, :login, :password)", {
                'id': id,
                'login': ara[7],
                'password': ara[8]
            })

        with self.connection:
            for i in self.subjects:
                self.cursor.execute(f"INSERT INTO std{id} VALUES (:subject, :mark)",
                                    {'subject': i, 'mark': 0})

    def addAdmin(self):
        login = str(input('Login: '))
        passwd = str(input('Passwd: '))
        conn = sqlite3.connect('Database/admins.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        with conn:
            cursor.execute("INSERT INTO admins VALUES (:login, :password)", {
                'login': login,
                'password': passwd})

    def addSubject(self, subject):
        with self.connection:
            self.cursor.execute(f"INSERT INTO std{self.getID()} VALUES (:subject, :mark)",
                                {'subject': subject, 'mark': 0})

    def changeMark(self, std, mark, subj):
        mark = int(mark)
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
            writer = pd.ExcelWriter(f'{subject}.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name=group)
            if group not in os.listdir('temp'):
                os.mkdir(f'temp/{group}')
            os.chdir(f'temp/{group}')
            writer.save()
            os.chdir(root)
            return df
        else:
            subj = []
            mark = []
            for i in self.cursor.execute(f"SELECT * FROM std{self.getID()}"):
                subj.append(i['subject'])
                mark.append(i['mark'])
            df = pd.DataFrame({'Предмет': subj, 'Оцінка': mark}, index=[i for i in range(1, len(mark) + 1)])
            return repr(df)

    def StdInfo(self, std):
        big_str = ''
        data1 = ['Фамілія', "Ім'я", 'Вік', 'Факультет', 'Група', 'Курс', 'Контракт']
        data2 = []
        self.cursor.execute(f"SELECT * FROM students WHERE firstname=:firstname", {'firstname': std.split(' ')[0]})
        main = self.cursor.fetchone()
        for i in main:
            data2.append(i)
        data2 = data2[1:]
        for i in range(len(data2)):
            big_str += f'{data1[i]}: {data2[i]}\n'
        return big_str

    def excelDBread(self, group, subject):
        df = pd.read_excel(f'temp/{group}/{subject}.xlsx', sheet_name=group)
        for i in df.index:
            self.changeMark(df['Студент'][i], df['Оцінка'][i], subject)

    def del_std(self, std):
        std1 = std.split(' ')
        id = self.getID(std)
        with self.connection:
            self.cursor.execute("DELETE FROM students WHERE firstname=:firstname AND lastname=:lastname", {
                'firstname': std1[0],
                'lastname': std1[1]
            })
            self.cursor.execute(f"DROP TABLE std{id}")

        connection = sqlite3.connect("Database/passwd.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        with connection:
            cursor.execute("DELETE FROM passwd WHERE id=:id", {'id': id})

    def changeCourse(self, std, course):
        self.cursor.execute(f"UPDATE students SET course=:course WHERE firstname=:firstname",
                            {'course': course, 'firstname': std.split(' ')[0]})

    def changeGroup(self, std, group):
        self.cursor.execute(f"UPDATE students SET group=:group WHERE firstname=:firstname",
                            {'group': group, 'firstname': std.split(' ')[0]})

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


def getNamesOfTeach():
    connection = sqlite3.connect("Database/teachers.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    teach = []
    for i in cursor.execute(f'SELECT * FROM teachers'):
        teach.append(f"{i['firstname']} {i['lastname']}")
    connection.close()
    return teach


def getpasswdstd():
    conn = sqlite3.connect("Database/passwd.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    data = {}
    std = getNamesOfSTD()
    for i, j in enumerate(cursor.execute(f"SELECT * FROM passwd")):
        data[std[i]] = j['password']
    return data


def getpasswdteach():
    conn = sqlite3.connect("Database/teachers.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    data = {}
    teach = getNamesOfTeach()
    for i, j in enumerate(cursor.execute(f"SELECT * FROM teachers")):
        data[teach[i]] = j['passwd']
    return data


if __name__ == '__main__':
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
    # conn = sqlite3.connect('Database/admins.db')
    # conn.row_factory = sqlite3.Row
    # cursor = conn.cursor()
    # cursor.execute("""CREATE TABLE admins(
    #     login text,
    #     password text
    # )""")
    # pass
    db = Database()
    db.del_std('Троцюк Павло')
