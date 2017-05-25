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
        #self.arrival_time = int(random.expovariate(lamd) + current_time)
        #self.compute_arrival(current_time)
        self.compute_exponent(current_time)
        self.customer_number = customer_number
        self.leave_queue = random.randint(5, 8)
        self.pay_time = int(random.random() * 120)
        self.take_time = int(random.random() * 120)
        self.order = Order(self.customer_number)

    # def compute_arrival(self, current_time):
    #     self.arrival_time = int(random.expovariate(lamd) + current_time)
    #     if(self.arrival_time == current_time):
    #         self.arrival_time = current_time + 1

    def compute_exponent(self,current_time):
        global lamd
        if current_time > 7200 and current_time % 1500 ==0:
            lamd+=5
        elif current_time % 1500 == 0 and current_time >0:
            lamd-=5
        arrive = int(random.expovariate(1.0/lamd) + current_time)
        if arrive == current_time:
            arrive+=1
        self.arrival_time= arrive



class Order:
    def __init__(self, customer_number):
        self.preapere_time = int(random.random() * 96)
        self.customer_number = customer_number
        self.order_value = int(random.random() * 1000)
        self.delay_at_desk = random.randint(1, 10)
        self.ready_to_cook = False


def first_line():
    print('Code for the first line')


def is_sitting_clear(sitting_area):
    """
    Check if there is room in the sitting area
    """
    for i in sitting_area:
        if i is None:
            return True
    return False


def enter_sitting(sitting_area, customer):
    """
    Move the customer into the sitting area
    """
    for i in sitting_area:
        if i is None:
            sitting_area[sitting_area.index(i)] = customer
            break


def is_reception_clear(reception_desk):
    if reception_desk[0] is None:
        return True
    else:
        return False

def sitting_area_count(sitting_area):
    count = 0
    for i in sitting_area:
        if i is not None:
            count+=1
    return count


def sitting_queue(sitting_area, kitchen, i, finished_orders, reception_desk):
    # A copy of the kitchen list, in order to be able to modify the original
    # kitchen during the loop
    for order in list(kitchen):
        if order.delay_at_desk == i:
            order.preapere_time += i
            order.ready_to_cook = True
        if order.preapere_time <= i and order.ready_to_cook:
            global kitchen_finished
            kitchen_finished+=1
            finished_orders.append(order)
            kitchen.remove(order)
    # Check if the reception desk is clear
    if is_reception_clear(reception_desk):
        # Now call a customer to take an order
        find = False
        for order in list(finished_orders):
            for customer in list(sitting_area):
                if customer is not None:
                    if order.customer_number == customer.customer_number:
                        # finished_orders.remove(order)
                        customer.take_time += i
                        reception_desk[0] = customer
                        print("The customer {} is now at the food reception desk".format(
                            customer.customer_number))
                        sitting_area[sitting_area.index(customer)] = None
                        find = True
                        break
            if find:
                break
    else:
        if reception_desk[0].take_time <= i:
            customer = reception_desk[0]
            reception_desk[0] = None
            global receive_count
            receive_count+=1
            print("{} Customer {} has received food and left the restaurant".format(
                i, customer.customer_number))


def main_loop(duration):
    customer = 0
    customer_number = 0
    queue = collections.deque()  # The first line
    paying_queue = collections.deque(maxlen=1)
    paying_queue.clear()
    paying_customer = 0
    kitchen = list()    # The orders
    sitting_area = [None for _ in range(5)]    # The second line
    finished_orders = list()
    reception_desk = [None]
    customers_left_billing_counter = 0
    for i in range(0, duration):
        # Caclculate statistics
        if i % 20 == 0 and i > 0:
            global billing_counter_efficiency
            if customers_left_billing_counter > 0:
                billing_counter_efficiency = (
                    (billing_counter_efficiency * (i - 20)) + (customers_left_billing_counter * 20)) / i
                customers_left_billing_counter = 0
            global billing_counter_waiting_in_line
            billing_counter_waiting_in_line = ((billing_counter_waiting_in_line * (i - 20)) + (len(queue) * 20)) / i
            global kitchen_efficency
            global kitchen_finished
            if kitchen_finished >0:
                kitchen_efficency = ((kitchen_efficency*(i-20)) + (kitchen_finished*20))/i
                kitchen_finished=0
            global kitchen_waiting_in_line
            if len(kitchen) > 0:
                kitchen_waiting_in_line = ((kitchen_waiting_in_line*(i-20))+ (len(kitchen)* 20))/i
            global order_recieve_counter_efficiency
            global receive_count
            if receive_count > 0:
                order_recieve_counter_efficiency = ((order_recieve_counter_efficiency*(i-20)) + (receive_count * 20))/i
                receive_count=0
            global order_recieve_counter_waiting_in_line
            order_recieve_counter_waiting_in_line = ((order_recieve_counter_waiting_in_line*(i-20)) + (sitting_area_count(sitting_area)*20))/i
            

        # Code for the first line #############################################
        if customer == 0:
            customer_number += 1
            global total_customers
            total_customers += 1
            customer = Customer(i, customer_number)
            print("{}: Customer {} will arrive at {}".format(
                i, customer.customer_number, customer.arrival_time))
        else:
            if customer.arrival_time == i:
                # the queue is too long for that customer, he decided to leave
                if customer.leave_queue <= len(queue):
                    print("{}: Customer {} has decided to leave the restaurant because the queue is too long".format(
                        i, customer.customer_number))
                    global total_loss
                    total_loss += customer.order.order_value
                    customer = 0
                else:
                    queue.append(customer)
                    print("{}: Customer {} has arrived, he is now standing in the line to order".format(
                        i, customer.customer_number))
                    global total_gain
                    total_gain += customer.order.order_value
                    customer = 0
        if len(paying_queue) == 0:  # no customer is paying
            if len(queue) != 0:
                paying_customer = queue.popleft()
                paying_customer.pay_time += i
                # The first customer in line if going to start paying
                paying_queue.append(paying_customer)
                print("{}: Customer {} is starting to pay".format(
                    i, paying_customer.customer_number))
        else:
            if paying_customer.pay_time == i:
                # Move customer to the waiting for food queue.
                print("{}: Customer {} is finished paying".format(
                    i, paying_customer.customer_number))
                paying_customer.order.delay_at_desk += i
                kitchen.append(paying_customer.order)
                if is_sitting_clear(sitting_area):
                    print("{}: Customer {} is going to wait for food".format(
                        i, paying_customer.customer_number))
                    paying_queue.clear()
                    enter_sitting(sitting_area, paying_customer)
                    customers_left_billing_counter += 1
                else:
                    print("{}: There is no room in the sitting area!".format(i))
                    print("Customer {} will wait at the counter until there is room".format(
                        paying_customer.customer_number))
            elif paying_customer.pay_time < i:
                if is_sitting_clear(sitting_area):
                    print("{}: Customer {} is going to wait for food, his food will be rady in {}".format(
                        i, paying_customer.customer_number, paying_customer.order.preapere_time))
                    paying_queue.clear()
                    enter_sitting(sitting_area, paying_customer)
                    customers_left_billing_counter += 1
                else:
                    print("{}: There is no room in the sitting area!".format(i))
                    print("Customer {} will wait at the counter until there is room".format(
                        paying_customer.customer_number))

            # elif paying_customer.pay_time > i:
            #     if(is_sitting_clear(sitting_area)):
            #         print("{}: Customer {} is going to wait for food".format(
            #             i, paying_customer.customer_number))
            #         paying_queue.clear()
            #         enter_sitting(sitting_area, customer)
                ###############################################################
        """
        Code for The second queueu
        """
        sitting_queue(sitting_area, kitchen, i,
                      finished_orders, reception_desk)


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
    global lamd
    print(duration)
    if choice == 1:
        print("--------------Morning simulation---------------")
        lamd = 100
    elif choice == 2:
        print("---------------Noon simulation-----------------")
        lamd = 80
    else:
        print("--------------Evening simulation---------------")
        lamd = 50
    global total_duration
    total_duration = duration / 3600
    main_loop(duration)


lamd = 0
##########################################################################
total_customers = 0
total_duration = 0
total_gain = 0
total_loss = 0
###########################################
billing_counter_efficiency = 0.0
kitchen_efficency = 0.0
order_recieve_counter_efficiency = 0.0
billing_counter_waiting_in_line = 0.0
kitchen_waiting_in_line = 0.0
order_recieve_counter_waiting_in_line = 0.0
###########################################
receive_count=0
kitchen_finished = 0

main()


print("###################################Simulation conculusion###################################")
print("Total duration: {} hours".format(total_duration))
print("Total customers: {}".format(total_customers))
print("Total gain: {} rupees".format(total_gain))
print("Total loss: {} rupees".format(total_loss))
print("Billing counter efficency: {}".format(billing_counter_efficiency))
print("Billing counter waiting in line: {}".format(
    billing_counter_waiting_in_line))
print("Kitchen efficency: {}".format(kitchen_efficency/(total_duration)))
print("Kitchen waiting in line: {}".format(kitchen_waiting_in_line))
print("Order receive counter efficency: {}".format(order_recieve_counter_efficiency))
print("Order receive counter waiting in line: {}".format(order_recieve_counter_waiting_in_line))
