import os
from peewee import *

if os.environ.get('ENV') == 'production':
    db = PostgresqlDatabase(
        'kicknews_db', 
        user='kicknews', 
        password=os.environ.get('DB_PWD'), 
        host=os.environ.get('DB_URL')
    )
else:
    db = SqliteDatabase('news.db')

class BaseModel(Model):
    class Meta:
        database = db

class Search(BaseModel):
    search = CharField()

class News(BaseModel):
    search = ForeignKeyField(Search, backref="news")
    title = CharField()
    url = CharField()
    text = CharField()
    date = CharField()
    saved_date = DateTimeField()

db.create_tables([Search, News])
