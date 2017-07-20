"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    # TODO: need to implement this

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Customer: %s, %s, %s, %s>" % (self.first_name, self.last_name, self.email, self.password)

def get_customer_info():
    customers = open("customers.txt")
    customer_info = {}
    for customer in customers:
        customer = customer.rstrip()
        customer = customer.split("|")
        f_name, l_name, email_add, password = customer
        customer_info[email_add] = Customer(f_name, l_name, email_add, password)

    return customer_info

def get_by_email(email):
    try:
        cust = customers[email]
    except:
        cust = False
    return cust

customers = get_customer_info()
