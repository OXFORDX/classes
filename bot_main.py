import sqlite3
import random


class Database:
    def __init__(self, flname):
        rand = flname.split(' ')
        self.fname = rand[0]
        self.lname = rand[1]
        self.connection = sqlite3.connect("database.db")
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
        self.connection.commit()

    def addSubject(self, subject):
        with self.connection:
            self.cursor.execute(f"INSERT INTO std{self.getID()} VALUES (:subject, :mark)",
                                {'subject': subject, 'mark': 0})

    def changeMark(self, subject, mark):
        mark = int(mark)
        with self.connection:
            self.cursor.execute(f"UPDATE std{self.getID()} SET mark=:mark WHERE subject=:subject", {
                'mark': mark,
                'subject': subject
            })

    def getID(self):
        self.cursor.execute(f"""SELECT id FROM students WHERE firstname=:firstname AND lastname=:lastname""",
                            {'firstname': self.fname, 'lastname': self.lname})
        obj = self.cursor.fetchone()
        return obj['id']

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


subjects = ['Математика', 'КПЗ', 'Психологія', 'Філософія', 'Веб-програмування']
db = Database('Ямковий Андрій')
db.changeMark('Математика', 30)
for i in subjects:
    db.addSubject(i)
generateMarks(db, subjects)
