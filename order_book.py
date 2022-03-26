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

    session.query(Order).filter(Order.filled == None, Order.buy_currency == new_order.sell_currency,
                                Order.sell_currency == new_order.buy_currency,
                                Order.sell_amount / Order.buy_amount <= new_order.buy_amount / new_order.buy_amount)
    #How to do  The buy / sell amounts need not match exactly and Each order should match at most one other

    Order.tx_id = Column(String(256))
    Order.signature = Column(String(256))
    Order.timestamp = Column(DateTime, default=datetime.now())  # When was the order inserted into the database
    Order.counterparty_id = Column(Integer, ForeignKey(
        'orders.id'))  # If the order was filled (or partially filled) the order_id of the order that acted as the counterparty
    Order.counterparty = relationship("Order",
                                foreign_keys='Order.counterparty_id')  # The Order object referenced by counterparty_id
    Order.filled = Column(DateTime)  # When was the order filled
    Order.creator_id = Column(Integer, ForeignKey(
        'orders.id'))  # For derived orders: the order ID of the order that this order was derived from
    Order.child = relationship("Order", foreign_keys='Order.creator_id', backref=backref('creator', remote_side=[
        id]))  # set "child" and "creator" to be the derived Order and creating Order objects associated.

    pass