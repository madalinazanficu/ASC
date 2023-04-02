"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

        # Thread initialization
        Thread.__init__(self, **kwargs)

        # Each consumer has a list of products purchased
        self.products_purchased = []

    def run(self):
        # Purchase stage
        for cart in self.carts:

            # Generate the id for the current cart
            cart_id = self.marketplace.new_cart()

            # Each cart has a list of operations
            for operation in cart:
                action = operation['type']
                product = operation['product']
                quantity = operation['quantity']

                # Try to add/remove the desired quantity of the current product
                for q in range(quantity):

                    if action == "add":
                        added = self.marketplace.add_to_cart(cart_id, product)

                        # Wait until you are able to add the product to your cart
                        while not added:
                            sleep(self.retry_wait_time)
                            added = self.marketplace.add_to_cart(cart_id, product)

                    elif action == "remove":
                        removed = self.marketplace.remove_from_cart(cart_id, product)
            
            # All operations for the current cart are done => place the order
            all_products = []
            all_products = self.marketplace.place_order(cart_id)
           
           
                
                    
                   

