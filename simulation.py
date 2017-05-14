# import simpy


# def car(env):
#     while True:
#         print('Start parking at %d' % env.now)
#         parking_duration = 5
#         yield env.timeout(parking_duration)

#         print('Start driving at %d' % env.now)
#         trip_duration = 2
#         yield env.timeout(trip_duration)


# env = simpy.Environment()
# env.process(car(env))
# env.run(until=15)

import random
import numpy
import collections


class Customer:
    """
    Customer class
    """

    def __init__(self, current_time, customer_number):
        self.arrival_time = numpy.random.exponential(
            scale=1.0, size=None) + current_time
        self.order_value = random.randint(200, 100)
        self.customer_number = customer_number
        self.leave_queue = random.randint(900, 2400)
        self.pay_time = int(random.random() * 140)
        self.order = Order()


class Order:
    def __init__(self, customer_number):
        self.preapere_time = int(random.random() * 120)
        self.customer_number = customer_number


def first_line():
    print('Code for the first line')


def main_loop(duration):
    customer = 0
    customer_number = 0
    queue = collections.deque()
    for i in range(0, duration):
        # Code for the first line #############################################
        if customer is 0:
            customer_number += 1
            customer = Customer(i, customer_number)
            if customer.arrival_time is i:
                queue.append(customer)
                print('Adding customer ' +
                      customer.customer_number + ' to the line')
                customer = 0
        #######################################################################


def main():
    choice = 0
    duration = 0
    while True:
        print("Please choose the time in day")
        print("1. Morning")
        print("2. Noon")
        print("3. Evening")
        choice = int(input())
        if choice == 1 or choice == 2 or choice == 3:
            break

    while True:
        print("Please enter the duration of simulation in hours (1-4)")
        duration = int(input())
        if duration >= 0 and duration <= 4:
            break

    if choice == 1:
        print("--------------Morning simulation---------------")
    elif choice == 2:
        print("---------------Noon simulation-----------------")
    else:
        print("--------------Evening simulation---------------")


main()
