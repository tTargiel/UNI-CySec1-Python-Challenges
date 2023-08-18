import random
from hashlib import md5 as md5

debug = False

# Menu
pizzas = ["Margherita", "Salami", "MexicanHot", "4Cheese", "GreenGarden"]

# Order radius
max_lat, min_lat = 49.357763860575986, 49.19837207080184
max_long, min_long = 7.138406298834504, 6.805607416509137

# Location for getting the flag
cispa_location = [49.2593251070081, 7.051249298056686]
cispa_error = 0.0007

# Load lists for simulating orders by a random human -> userid is not mapped to one name
with open("resources/firstnames.txt", "r") as f:
    firstnames = f.read().split("\n")

with open("resources/surnames.txt", "r") as f:
    surnames = f.read().split("\n")

with open("resources/emails.txt", "r") as f:
    email_domains = f.read().split("\n")


class Pizzeria:
    shared_secret = b""
    flag = ""

    def __init__(self, secret, flag):
        '''
        Args:
            secret: the shared secret used for hashing
            flag: the flag a hacker would receive
        '''
        self.shared_secret = secret.encode("utf-8")
        self.flag = flag

    def orderToDict(self, order):
        '''
        Args:
            order: as a string

        Returns:
            Tuple of dictionary of parameters and None if it worked
            or
            Tuple of None and a message if some parameter was missing or something
        '''
        order_dict = {}

        # Separate parameters
        order_split = order.split("&")

        # Check if there were any parameters at all
        if len(order_split) == 0:
            return None, "ORDER FAILED: You probably did not read the tutorial on how to order pizza"

        # Separate parameter name and value
        order_split = [x.split("=") for x in order_split]

        # Built dictionary
        for param in order_split:
            if len(param) < 2:
                return None, f"ORDER FAILED: Parameter {param} has no value"

            order_dict[param[0]] = param[1]

        return order_dict, None

    def getUser(self):
        '''
        Creates a random person + an email address with hidden characters
        (userid is not mapped to one person!!!)
        Returns:
            Tuple of persons first name and surname and his email, both as a string
        '''
        firstname = random.choice(firstnames)
        surname = random.choice(surnames)
        mail = firstname[:2].lower() + "*" * random.randint(4, 10) + random.choice(email_domains)
        return (firstname + " " + surname, mail)

    def receiveOrder(self, order, order_hash):
        '''
        Models something like the routine for receiving requests
        Args:
            order: as bytes
            order_hash: as bytes

        Returns:
            Tuple with the answer of the "server" and the checksum
        '''

        h = md5(self.shared_secret + order).hexdigest()

        # Check hash
        if h != order_hash.decode("UTF-8"):
            if debug: print(f"Hash received: {order_hash}")
            if debug: print(f"Hash expected: {order_hash}")
            msg = f"ORDER FAILED: Order does not match the hash! Received hash {order_hash}, expected {h}."
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Decode Order
        try:
            # Check for every byte if it is a valid character (there could be broken bits due to transmission)
            char_list = []
            for b in order:
                try:
                    char_list.append(chr(b))
                except:
                    continue
            order = "".join(char_list)
        except:
            msg = "ORDER FAILED: Encoding of the order is broken"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        if debug: print(f"Order: {order}")
        if debug: print(f"Hash: {order_hash}")

        # Check order params
        order_dict, msg = self.orderToDict(order)
        if not order_dict:
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # --- Check order details ---
        # Check if pizza param exists
        if "pizza" not in order_dict.keys():
            msg = "ORDER FAILED: No pizza in order"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Check if pizza exists in menu
        pizza = order_dict["pizza"]
        if pizza not in pizzas:
            msg = "ORDER FAILED: Sorry we don't have this type of pizza"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Check if userid param exists
        if "userid" not in order_dict.keys():
            msg = "ORDER FAILED: Missing userid"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Check right format
        userid = order_dict["userid"]
        if not userid.isalnum():
            msg = f"ORDER FAILED: Sorry user with id must be an integer"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        userid = int(userid)

        # Check if in range
        if userid > 63527801 or userid < 1:
            msg = f"ORDER FAILED: Sorry user with id {userid} is not registered"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # --- Check location ---
        # Check if lat param exists
        if "lat" not in order_dict.keys():
            msg = "ORDER FAILED: Missing lat"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()
        lat = order_dict["lat"]

        # Check right format
        try:
            lat = float(lat)
        except:
            msg = f"ORDER FAILED: Sorry lat must be of type float"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Check if in range
        if lat > max_lat or lat < min_lat:
            msg = f"ORDER FAILED: Sorry we do not deliver to this location"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Check if long param exists
        if "long" not in order_dict.keys():
            msg = "ORDER FAILED: Missing long"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()
        long = order_dict["long"]

        # Check right format
        try:
            long = float(long)
        except:
            msg = f"ORDER FAILED: Sorry long must be of type float"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Check if in range
        if long > max_long or long < min_long:
            msg = f"ORDER FAILED: Sorry we do not deliver to this location"
            return msg.encode("utf-8"), md5(msg.encode("UTF-8")).digest()

        # Check flag should get attached
        flag_line = ""
        # Check for cispa entrance
        if lat < cispa_location[0] + cispa_error and lat > cispa_location[0] - cispa_error:
            if long < cispa_location[1] + cispa_error and long > cispa_location[1] - cispa_error:
                flag_line = f"Flag: {self.flag}\n"

        user = self.getUser()

        order_details = f"------------------- Order excepted -------------------\n" \
                        f"Name:         {user[0]}\n" \
                        f"Order:        1x {pizza}\n" \
                        f"Location:     {lat}, {long}\n" \
                        f"Payment:      Paypal {user[1]}\n" \
                        f"{flag_line}" \
                        f"Will be delivered in {random.randint(15, 45)} min\n" \
                        f"------------------------------------------------------"

        return order_details.encode("utf-8"), md5(order_details.encode("UTF-8")).digest()
