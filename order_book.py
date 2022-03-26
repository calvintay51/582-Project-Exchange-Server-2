from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    # print(order)
    #Your code here
    # Order.buy_currency = order["buy_currency"]
    # Order.sell_currency = order["sell_currency"]
    # Order.buy_amount = order["buy_amount"]
    # Order.sell_amount = order["sell_amount"]
    # Order.receiver_pk = order["receiver_pk"]
    # Order.sender_pk = order["sender_pk"]
    new_order = add_new_order(order)


    remaining_buy = order["buy_amount"]
    # print(remaining_buy)

    while remaining_buy != 0:
        session.query(Order).order_by(Order.sell_amount / Order.buy_amount).all()

        matched_orders = session.query(Order).filter(Order.filled == None, Order.buy_currency == order["sell_currency"],
                                                 Order.sell_currency == order["buy_currency"],
                                                 Order.sell_amount / Order.buy_amount <= order["buy_amount"] / order["sell_amount"]).all()

        if len(matched_orders) == 0:
            break
        else:
            # print("traded")
            best_match = matched_orders[-1]
            filled_time = datetime.now()
            best_match.filled = filled_time
            new_order.filled = filled_time
            best_match.counterparty_id = new_order.id
            new_order.counterparty_id = best_match.id

            replacement_order = None
            if best_match.sell_amount > new_order.buy_amount:
                exchg = best_match.buy_amount / best_match.sell_amount

                replacement_order = Order(buy_currency=best_match.buy_currency, sell_currency=best_match.sell_currency,
                                          buy_amount=best_match.buy_amount - new_order.buy_amount * exchg,
                                          sell_amount=best_match.sell_amount - new_order.buy_amount,
                                          receiver_pk= best_match.receiver_pk, sender_pk= best_match.sender_pk,
                                          creator_id = best_match.id)

                exchg1 = replacement_order.buy_amount / replacement_order.sell_amount
                print("comp", exchg, exchg1)
                session.add(replacement_order)
                session.commit()

            elif best_match.sell_amount < new_order.buy_amount:
                exchg = new_order.buy_amount / new_order.sell_amount

                replacement_order = Order(buy_currency=new_order.buy_currency, sell_currency=new_order.sell_currency,
                                          buy_amount=new_order.buy_amount - best_match.sell_amount,
                                          sell_amount=new_order.sell_amount - best_match.sell_amount / exchg,
                                          receiver_pk= new_order.receiver_pk,sender_pk= new_order.sender_pk,
                                          creator_id=new_order.id)
                exchg1 = replacement_order.buy_amount / replacement_order.sell_amount
                print("comp1", exchg, exchg1)
                session.add(replacement_order)
                session.commit()


            break


    # print("trade")
    # if len(matched_orders) >0:
    #     # print(matched_orders[1])
    #     # pass
    #     for i in matched_orders:
    #         print(i.sell_currency, i.sell_amount, i.buy_currency, i.buy_amount)

    #search for a matching order
    # matched_orders = session.query(Order).filter(Order.filled == None, Order.buy_currency.like(new_order.sell_currency)) #,\
                    # Order.sell_currency == new_order.buy_currency, Order.sell_amount / Order.buy_amount <= new_order.buy_amount / new_order.buy_amount)
    #How to do  The buy / sell amounts need not match exactly and Each order should match at most one other

    # session.query.order_by(session.total.desc()).all()
    # print(matched_orders)



def add_new_order(order):
    new_order = Order(buy_currency = order["buy_currency"],sell_currency = order["sell_currency"],
                buy_amount = order["buy_amount"], sell_amount = order["sell_amount"], receiver_pk = order["receiver_pk"],
                sender_pk=order["sender_pk"])
    session.add(new_order)
    session.commit()
    return new_order