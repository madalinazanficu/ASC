"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

        # Thread initialization
        Thread.__init__(self, **kwargs)

    def run(self):
        # Producer Registration
        producer_id = self.marketplace.register_producer()

        # Pubish products continously
        while True:
            for product in self.products:

                # Try to publish this quantity of the current product
                quantity = int(product[1])
                while quantity > 0:

                    published = self.marketplace.publish(producer_id, product[0])

                    # If the marketplace is full, wait and try again
                    while not published:
                        sleep(self.republish_wait_time)
                        published = self.marketplace.publish(producer_id, product[0])

                    # Wait until to publish something else
                    sleep(product[2])
                    quantity -= 1
