#!/usr/bin/env python

from pizzeria import Pizzeria
from customer import Customer
from hle import HashLengthExtension


# CustomerInterface and PizzaInterface allow tests to have access to the messages
# -> Calling the functions of customer and pizzeria does not work due to the randomness
# Works like a (very small :D) stack for network communication
class CustomerInterface:
    msg = ""
    hash = ""

    def __init__(self, secret):
        self.__customer = Customer(secret)

    def send(self, msg, hash):
        self.msg = msg
        self.hash = hash

    def receive(self):
        self.msg, self.hash = self.__customer.send()
        return self.msg, self.hash


class PizzeriaInterface:
    msg = ""
    hash = ""

    def __init__(self, secret, flag):
        self.__pizzeria = Pizzeria(secret, flag)

    def send(self, msg, hash):
        self.msg, self.hash = self.__pizzeria.receiveOrder(msg, hash)

    def receive(self):
        return self.msg, self.hash


def main():
    shared_secret = "yLWjEVR9950Pmhmupaqgtz8fYSTTGpcJ"  # 32 byte long secret
    flag = "CYSEC{The pizza is not a lie!}"

    c = CustomerInterface(shared_secret)
    p = PizzeriaInterface(shared_secret, flag)

    # Run attack
    HashLengthExtension(c, p).attack()

    # Check if attack worked
    final_msg, final_hash = p.receive()
    if flag in final_msg.decode("UTF-8"):
        print("It worked :D")
    else:
        print("It didn't work :(")


if __name__ == '__main__':
    main()
