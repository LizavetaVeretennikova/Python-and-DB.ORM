import json
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

with open('fixtures/tests_data.json', 'r') as f:
    data = json.load(f)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


#publisher_1 = Publisher(name="Пушкин Александр Сергеевич")
#session.add(publisher_1)
#session.commit()

#book_1 = Book(title="Капитанская дочка", id_publisher=1)
#session.add(book_1)
#session.commit()

#shop_1 = Shop(name="Буквоед")
#session.add(shop_1)
#session.commit()

#stock_1 = Stock(id_book=1, id_shop=1, count=2)
#session.add(stock_1)
#session.commit()

#sale_1 = Sale(price=600, date_sale="09-11-2022", id_stock=1, count=3)
#session.add(sale_1)
#session.commit()

def get_shops(session, input_publisher):
    query = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale
    ).select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale)
    if input_publisher.isdigit():
        result = query.filter(Publisher.id == input_publisher).all()
    else:
        result = query.filter(Publisher.name == input_publisher).all()
    for title, name, price, date_sale in result:
        print(f"{title: <40} | {name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")
session.commit()

if __name__ == '__main__':
    input_publisher = input("Введите имя или id публициста: ")
    get_shops(session, input_publisher)
    session.close()