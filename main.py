import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import json
DSN = 'postgresql://postgres:MurakamI200408@localhost:5432/book_shop'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

#with open('tests_data.json', 'r') as fd:
 #   data = json.load(fd)

#for record in data:
 #   model = {
  #      'publisher': Publisher,
   #     'shop': Shop,
    #    'book': Book,
     #   'stock': Stock,
      #  'sale': Sale,
    #}[record.get('model')]
    #session.add(model(id=record.get('pk'), **record.get('fields')))
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
for title, name, price, date_sale in session.query(Publisher).join(Book.title, Shop.name, Sale.price, Sale.date_sale).filter(Publisher.like(f"%{input_}%")).all():
    print(f"{title} | {name} | {price} | {date_sale}")

#for c in session.query(Publisher).filter(Publisher.name.like('%Пушкин%')).all():
#    print(c)
session.commit()


session.close()