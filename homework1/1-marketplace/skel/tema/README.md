### Zanficu Madalina-Valetina 333CA
## Computer systems architecture - Homework 1

### I. Structure 

The program follows the approach to the classical ***Multiple Producers -Multiple Consumers*** 
problem from Parallel and Distributed algorithms.

a. ***Homework utility*** <br/>
    TODO:

b. ***Design choices and code snipptes***                                       <br/>
My solution is based on manipulating the data stuctures described below,      
and also on thread synchronization using mutexes.                               

- **1. Buffer** is a dictitionary which maintains the products as keys          
and each key is associated with a list of producers:                            <br/>
{                                                                               <br/>
    Tea     -> Producer0, Producer1, Producer2                                  <br/>
    Coffee  -> Producer1, Producer2                                             <br/>
    ...                                                                         <br/>
}                                                                               <br/>
**Usage**: everytime a producer publish something, this resource is added
to the buffer dictionary from where all consumers are able to buy it
based on the product type.

- **2. Producers** dictionary's role is to keep track of each producer production.
Each producer has a publishing limit, so everytime a product is either 
published, added to a cart or removed from a cart, the production is affected.

The key is producer_id and the value is the number of published products.       <br/>
{                                                                               <br/>
    Producer0 -> 2                                                              <br/>
    Producer1 -> 5                                                              <br/>
    Producer2 -> 3                                                              <br/>
    ...                                                                         <br/>
}                                                                               <br/>

- **3. Cart** looks like this:
{
    Cart1 -> [(Producer0, Coffee), (Producer0, Tea), (Producer2, Tea)]
    Cart2 -> [(Producer0, Coffee), (Producer0, Tea), (Producer2, Tea)]
    ...
}
**Usage**: everytime a product is removed from a cart, I need to know 
the producer of that product because the product need to be inserted 
back in the **buffer** and the **producer** production limit is affected.

**Mutex sitautions**:
1. Multiple producers may want to publish their product in the same time.
In order to do this they access **buffer[product]**, which is mapped
with multiple producers.

self.consume_lock.acquire()                                                        <br/>
self.buffer[product].append(producer)                                              <br/>
self.consume_lock.release()                                                        <br/>

2. Multiple consumers may want to add to their cart the same product.
The product is removed from **buffer[product]** => I need to make sure
each consumer pop a different product.

self.consume_lock.acquire()                                                        <br/>
producer = self.buffer[product].pop(0)                                             <br/>
self.consume_lock.release()                                                        <br/>

3. While printing the products from the cart in place_order stage.


c. ***Implementation efficiency***                                                <br/>
    TODO:


### II. Immplementation
    TODO: