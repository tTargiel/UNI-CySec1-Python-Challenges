import random
from hashlib import md5

debug = False

# Menu
pizzas = ["Margherita", "Salami", "MexicanHot", "4Cheese", "GreenGarden"]

# Order radius
max_lat, min_lat = 49.357763860575986, 49.19837207080184
max_long, min_long = 7.138406298834504, 6.805607416509137

# No orders to the University
blacklist_max_lat, blacklist_min_lat = 49.26102509484602, 49.24962304593174
blacklist_max_long, blacklist_min_long = 7.053275672273431, 7.029048462394631


class Customer:

    __shared_secret = b""

    def __init__(self, secret):
        '''
        Args:
            secret: the shared secret used for hashing
        '''
        self.__shared_secret = secret.encode("utf-8")

    def generateOrder(self):
        '''
        Returns:
            Generates a random get parameter like formatted order as a string
        '''

        # Random userid
        userid = random.randint(1, 63527801)

        # Random location
        while True:
            lat = random.uniform(min_lat, max_lat)
            if lat > blacklist_max_lat or lat < blacklist_min_lat:
                break

        while True:
            long = random.uniform(min_long, max_long)
            if long > blacklist_max_long or long < blacklist_min_long:
                break

        # Random pizza
        pizza = random.choice(pizzas)

        order = f"userid={userid}&pizza={pizza}&lat={lat}&long={long}"
        if debug: order = "userid=12117379&pizza=4Cheese&lat=49.31639559634483&long=6.877010186218736"
        # POV: You try to solve the challenge and find this line ^ ... might be helpful for debugging :)
        return order

    def send(self):
        '''
        Models something like the send button
        (normally this would start some network magic)
        Returns:
            Tuple of order and hash, both as bytes
        '''
        order = self.generateOrder().encode("utf-8")
        order_hash = md5(self.__shared_secret + order).hexdigest()

        if debug: print(f"Order:          {order}")
        if debug: print(f"Order hash:     {order_hash}")

        return order, order_hash.encode("UTF-8")
