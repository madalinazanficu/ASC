"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, Semaphore, Thread, currentThread 

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        # Each producer has a limit of production
        self.queue_size_per_producer = queue_size_per_producer

        # Producers dictionary maintains pairs {producer, published_products}
        self.producers = {}

        # The buffer dictionary keeps pairs {prod_type, [producer1, producer2, producer3...]}
        self.buffer = {}

        # The cart dictionary contains pairs {cart_id, [(producer1, product1), (producer2, product2)]}
        self.cart = {}

        # Register contors for producers and consumers
        self.order_id_producer = 0
        self.cart_id = 0

        # Locks and sync components
        self.register_lock = Lock()
        self.cart_lock = Lock()
        self.prod_lock = Lock()
        self.consume_lock = Lock()
        self.print_lock = Lock()

    
    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Multiple producers may want to register at the same time
        self.register_lock.acquire()
        self.order_id_producer += 1
        self.register_lock.release()

        # Add the producer in the dictionary
        self.producers[self.order_id_producer] = 0

        return self.order_id_producer


    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # The current producer has to wait until to publish again
        if self.producers[producer_id] >= self.queue_size_per_producer:
            return False
        
        # Multiple producers may want to publish their products simultaneous
        self.prod_lock.acquire()

        # Handle exception when the product is not in dictionary
        if product not in self.buffer:
            self.buffer[product] = []
        self.buffer[product].append(producer_id)
    
        self.prod_lock.release()

        # The quantity of products published by the producer is increased
        self.producers[producer_id] = self.producers[producer_id] + 1

        return True


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        # Multiple consumers may want to create a cart at the same time
        self.cart_lock.acquire()
        self.cart_id += 1
        self.cart_lock.release()

        # Add the cart in the dictionary
        self.cart[self.cart_id] = []

        return self.cart_id


    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        # Therse is no product of this type available
        if self.buffer.get(product) is None or len(self.buffer[product]) == 0:
            return False

        # The product is no longer available
        self.consume_lock.acquire()
        producer = self.buffer[product].pop(0)
        self.consume_lock.release()

        # Add the product to the cart
        entry_pair = (producer, product)
        self.cart[cart_id].append(entry_pair)

        # The product was added to cart => his producer can produce more
        self.producers[producer] = self.producers[producer] - 1
        
        return True


    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # Remove the product from customer's cart
        for entry_pair in self.cart[cart_id]:
            (entry_producer, entry_product) = entry_pair
            if entry_product == product:
                producer = entry_producer
                self.cart[cart_id].remove(entry_pair)
                break

        # Make this product available for other customers
        self.consume_lock.acquire()
        self.buffer[product].append(producer)
        self.consume_lock.release()

        # This affects the producer => he has a production limit
        self.producers[producer] = self.producers[producer] + 1


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        all_products = []

        # Extract the products from the cart
        for entry_pair in self.cart[cart_id]:
            (entry_producer, entry_product) = entry_pair
            all_products.append(entry_product)

        # Remove the cart from the dictionary
        del self.cart[cart_id]

        # Print the products
        for product in all_products:
            self.print_lock.acquire()
            print(f"{currentThread().getName()} bought {product}")
            self.print_lock.release()
    
        return all_products
