from orm.crabmodel import CrabModel, ForeignKey
from orm.datatypes import DataTypes


class Product(CrabModel):
    _column = {
        'title': DataTypes.varchar(max_length=30),
        'made_by': DataTypes.varchar(max_length=35),
        'created_at': DataTypes.datetimefield(auto_add_now=True)
    }