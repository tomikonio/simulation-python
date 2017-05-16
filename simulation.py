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
import collections

# Delay at kitchen is rand*96


class Customer:
    """
    Customer class
    """

    def __init__(self, current_time, customer_number):
        self.arrival_time = int(random.expovariate(0.01) + current_time)
        self.customer_number = customer_number
        self.leave_queue = random.randint(10, 50)
        self.pay_time = int(random.random() * 120)
        self.order = Order(self.customer_number)


class Order:
    def __init__(self, customer_number):
        self.preapere_time = int(random.random() * 96)
        self.customer_number = customer_number
        self.order_value = int(random.random() * 1000)


def first_line():
    print('Code for the first line')


def is_sitting_clear(sitting_area):
    for i in sitting_area:
        if i is None:
            return True
    return False


def enter_sitting(sitting_area, customer):
    for i in sitting_area:
        if i is None:
            sitting_area[sitting_area.index(i)] = customer
            break


def main_loop(duration):
    customer = 0
    customer_number = 0
    queue = collections.deque()
    paying_queue = collections.deque(maxlen=1)
    paying_queue.clear()
    paying_customer = 0
    kitchen = list()
    sitting_area = [None for _ in range(10)]
    for i in range(0, duration):
        # Code for the first line #############################################
        if customer == 0:
            customer_number += 1
            customer = Customer(i, customer_number)
            print("Customer " + str(customer.customer_number) +
                  " will arrive at " + str(customer.arrival_time))
        if customer != 0:
            if customer.arrival_time == i:
                queue.append(customer)
                print('Adding customer ' +
                      str(customer.customer_number) + ' to the line')
                customer = 0
        if len(paying_queue) == 0:  # no customer is paying
            if len(queue) != 0:
                paying_customer = queue.popleft()
                paying_customer.pay_time += i
                paying_queue.append(paying_customer)
        else:
            if paying_customer.pay_time == i:
                # Move customer to the waiting for food queue.
                print("Customer " + str(paying_customer.customer_number) +
                      " is finished paying")
                paying_customer.order.preapere_time += i
                kitchen.append(paying_customer.order)
                if(is_sitting_clear(sitting_area)):
                    print("Customer " + str(paying_customer.customer_number) +
                          " is going to wait for food")
                    paying_queue.clear()
                    enter_sitting(sitting_area, customer)

                ###############################################################


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

    duration *= 3600
    print(duration)
    if choice == 1:
        print("--------------Morning simulation---------------")
    elif choice == 2:
        print("---------------Noon simulation-----------------")
    else:
        print("--------------Evening simulation---------------")

    main_loop(duration)


main()
