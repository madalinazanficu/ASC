"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, Semaphore, Thread, currentThread
import unittest 
import tema.product

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


class TestMarketplace(unittest.TestCase):

    def setUp(self):
        queue_size_per_producer = 2
        self.market = Marketplace(queue_size_per_producer)

    # Test with 2 producers for registration
    def test_register_producer(self):
        producer_id1 = self.market.register_producer()
        producer_id2 = self.market.register_producer()

        self.assertEqual(producer_id1, 1)
        self.assertNotEqual(producer_id1, producer_id2)

    # Test with 1 producer and 1 product expecting True
    def test_publish_true(self):
        producer_id = self.market.register_producer()
        green_tea = product.Tea("Matcha", 5, "green")

        published = self.market.publish(producer_id, green_tea)
        self.assertTrue(published)


    # Test with 1 producer, 3 products exeeds the limit of 2
    def test_publish_exceed_limit(self):
        producer_id = self.market.register_producer()
        black_tea = product.Tea("Earl Grey", 5, "black")
        berries_tea = product.Tea("Raspberry Tea", 5, "berries")
        flat_white = product.Coffee("Flat White", 5, 5.05, "MEDIUM")

        self.market.publish(producer_id, black_tea)
        self.market.publish(producer_id, berries_tea)

        published = self.market.publish(producer_id, flat_white)
        self.assertFalse(published)


    # Test multiple producers pubblishing products, expecting True
    def test_publish_multiple_producers(self):
        producer_id1 = self.market.register_producer()
        producer_id2 = self.market.register_producer()
        green_tea = product.Tea("Matcha", 5, "green")
        ice_coffee = product.Coffee("Ice Coffee", 5, 4.05, "LOW")

        self.market.publish(producer_id1, green_tea)
        self.market.publish(producer_id2, ice_coffee)

        published1 = self.market.publish(producer_id1, green_tea)
        published2 = self.market.publish(producer_id2, ice_coffee)

        self.assertTrue(published1)
        self.assertTrue(published2)


    # Test with 2 consumers for registration, expecting 2 different ids
    def test_new_cart(self):
        cart_id1 = self.market.new_cart()
        cart_id2 = self.market.new_cart()

        self.assertEqual(cart_id1, 1)
        self.assertNotEqual(cart_id1, cart_id2)


    # Test that the product is not available in the buffer
    def test_add_to_cart_no_product(self):
        cart_id = self.market.new_cart()
        green_tea = product.Tea("Matcha", 5, "green")
        added = self.market.add_to_cart(cart_id, green_tea)

        self.assertFalse(added)

    # Test that the product is added to the cart and removed from the buffer
    def test_add_to_cart(self):
        producer_id = self.market.register_producer()
        green_tea = product.Tea("Matcha", 5, "green")
        self.market.publish(producer_id, green_tea)

        cart_id = self.market.new_cart()
        added = self.market.add_to_cart(cart_id, green_tea)

        self.assertTrue(added)
        self.assertEqual(len(self.market.cart[cart_id]), 1)
        self.assertEqual(len(self.market.buffer[green_tea]), 0)
        self.assertEqual(self.market.producers[producer_id], 0)

    # Test that the product is removed from the cart and added back to the buffer
    def test_remove_from_cart(self):
        producer_id = self.market.register_producer()
        green_tea = product.Tea("Matcha", 5, "green")
        self.market.publish(producer_id, green_tea)

        cart_id = self.market.new_cart()
        self.market.add_to_cart(cart_id, green_tea)
        self.market.remove_from_cart(cart_id, green_tea)

        self.assertEqual(len(self.market.cart[cart_id]), 0)
        self.assertEqual(len(self.market.buffer[green_tea]), 1)
        self.assertEqual(self.market.producers[producer_id], 1)
        

    # Test that the cart is empty after the order is placed
    def test_place_order(self):
        producer_id = self.market.register_producer()
        green_tea = product.Tea("Matcha", 5, "green")
        self.market.publish(producer_id, green_tea)
      
        cart_id = self.market.new_cart()
        self.market.add_to_cart(cart_id, green_tea)
        products = self.market.place_order(cart_id)

        self.assertEqual(len(products), 1)
        self.assertEqual(self.market.cart, {})


    # Test multiple functionalities
    def test_multiple(self):
        producer_id1 = self.market.register_producer()
        producer_id2 = self.market.register_producer()

        green_tea = product.Tea("Matcha", 5, "green")
        ice_coffee = product.Coffee("Ice Coffee", 5, 4.05, "LOW")

        self.market.publish(producer_id1, green_tea)
        self.market.publish(producer_id1, ice_coffee)
        self.market.publish(producer_id2, ice_coffee)
        self.market.publish(producer_id2, green_tea)

        cart_id1 = self.market.new_cart()

        self.market.add_to_cart(cart_id1, green_tea)
        self.market.add_to_cart(cart_id1, ice_coffee)

        # Test that the products are producted by the first producer
        self.assertEqual(self.market.cart[cart_id1], [(producer_id1, green_tea),
                                                      (producer_id1, ice_coffee)])
        
        self.assertEqual(self.market.producers[producer_id1], 0)
        

        # Remove from cart
        self.market.remove_from_cart(cart_id1, ice_coffee)
        self.assertEqual(self.market.cart[cart_id1], [(producer_id1, green_tea)])
        self.assertEqual(self.market.producers[producer_id1], 1)

        # Place order
        products = self.market.place_order(cart_id1)
        self.assertEqual(products, [green_tea])
        self.assertEqual(self.market.cart, {})

        

        