from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #Your code here
    # Order.buy_currency = order["buy_currency"]
    # Order.sell_currency = order["sell_currency"]
    # Order.buy_amount = order["buy_amount"]
    # Order.sell_amount = order["sell_amount"]
    # Order.receiver_pk = order["receiver_pk"]
    # Order.sender_pk = order["sender_pk"]
    new_order = Order(buy_currency = order["buy_currency"],sell_currency = order["sell_currency"],
                buy_amount = order["buy_amount"], sell_amount = order["sell_amount"], receiver_pk = order["receiver_pk"],
                sender_pk=order["sender_pk"])
    session.add(new_order)
    session.commit()


    #search for a matching order
    matched_orders = session.query(Order).filter(Order.filled == None, Order.buy_currency == new_order.sell_currency,
                                Order.sell_currency == new_order.buy_currency,
                                Order.sell_amount / Order.buy_amount <= new_order.buy_amount / new_order.buy_amount)
    #How to do  The buy / sell amounts need not match exactly and Each order should match at most one other

    session.query.order_by(session.total.desc()).all()
    print(matched_orders)


    pass