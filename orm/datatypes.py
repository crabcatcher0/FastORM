"""
    : Datatypes
"""


class DataTypes:
    
    @staticmethod
    def varchar(max_length=255):
        return f'VARCHAR({max_length}) NOT NULL'


    @staticmethod
    def integer():
        return 'INTEGER NOT NULL'


    @staticmethod
    def boolean():
        return 'BOOLEAN'


    @staticmethod
    def emailfield(unique = True):
        if unique:
            return 'VARCHAR(255) UNIQUE NOT NULL'
        else:
            return 'VARCHAR(255) UNIQUE NOT NULL'
    

    @staticmethod
    def datetimefield(auto_add_now=True):
        if auto_add_now:
            return  'DATETIME DEFAULT CURRENT_TIMESTAMP'
        



