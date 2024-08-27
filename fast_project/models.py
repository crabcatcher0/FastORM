from orm.crabmodel import CrabModel
from orm.datatypes import DataTypes


class Student(CrabModel):
    _column = {    
        'first_name': DataTypes.varchar(max_length=20),
        'last_name': DataTypes.varchar(max_length=20),
        'address': DataTypes.varchar(max_length=30),
        'email': DataTypes.emailfield(unique=True)
        }
    

class Course(CrabModel):
    _column = {
        'course_name': DataTypes.varchar(max_length=100),
        'course_code': DataTypes.varchar(max_length=10)
    }