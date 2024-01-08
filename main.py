#import json
import os
from dotenv import load_dotenv
load_dotenv()
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

secret_key = os.getenv("SECRET_KEY")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

DSN = f'postgresql://postgres:{secret_key}@{db_host}:{db_port}/book_shop'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

#with open('fixtures/tests_data.json', 'r') as fd:
#    data = json.load(fd)

#for record in data:
#    model = {
#        "publisher": Publisher,
#        "shop": Shop,
#        "book": Book,
#        "stock'": Stock,
#        "sale": Sale,
#    }[record.get('model')]
#    session.add(model(id=record.get('pk'), **record.get('fields')))
#session.commit()

publisher_1 = Publisher(name="Пушкин Александр Сергеевич")
session.add(publisher_1)
session.commit()

book_1 = Book(title="Капитанская дочка", id_publisher=1)
session.add(book_1)
session.commit()

shop_1 = Shop(name="Буквоед")
session.add(shop_1)
session.commit()

stock_1 = Stock(id_book=1, id_shop=1, count=2)
session.add(stock_1)
session.commit()

sale_1 = Sale(price=600, date_sale="09-11-2022", id_stock=1, count=3)
session.add(sale_1)
session.commit()
input_ = input("Введите имя автора: ")
def session_manager():

    #input_ = input("Введите имя автора: ")

    with session_manager() as session:
        query = session.query(Publisher, Book, Shop, Stock, Sale)
        query = query.join(Publisher, Publisher.id == Book.id_publisher)
        query = query.join(Book, Book.id_publisher == Publisher.id)
        query = query.join(Shop, Shop.id == Stock.id_shop)
        query = query.join(Stock, Stock.id_book == Book.id)
        query = query.join(Sale, Sale.id_stock == Stock.id)
        records = query.all()
    for title, name, price, date_sale in records.filter(Publisher.name.like(f"%{input_}%")):
        print(f"{title} | {name} | {price} | {date_sale}")

session.commit()


session.close()