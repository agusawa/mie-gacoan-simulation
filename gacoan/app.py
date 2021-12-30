import random
import sys
import time
import threading
from csv import DictWriter
from typing import List

import simpy

from gacoan import config
from gacoan.order import Order
from gacoan.queue import Queue
from gacoan.roles import Assembler, Boiler, Cashier, Fryer, Mixer, Topping
from gacoan.utils import monitor


class Gacoan:
    """
    Gacoan Simulation.
    """

    env: simpy.Environment
    csv_writer_per_minute: DictWriter
    csv_writer_customer: DictWriter

    num_arrivals = 0
    num_finished_orders = 0
    orders: List[int] = []

    # Resources
    assembler: Assembler
    boiler: Boiler
    cashier: Cashier
    fryer: Fryer
    mixer: Mixer
    topping: Topping

    # Queues
    assembler_queue: Queue
    boiler_queue: Queue
    cashier_queue: Queue
    fryer_queue: Queue
    mixer_queue: Queue
    topping_queue: Queue

    # Being served
    assembler_handle: Queue
    boiler_handle: Queue
    cashier_handle: Queue
    fryer_handle: Queue
    mixer_handle: Queue
    topping_handle: Queue

    def __init__(
        self,
        env: simpy.Environment,
        *,
        csv_writer_per_minute: DictWriter,
        csv_writer_customer: DictWriter
    ) -> None:
        self.env = env

        self.csv_writer_per_minute = csv_writer_per_minute
        self.csv_writer_customer = csv_writer_customer

        self.assembler_queue = Queue()
        self.boiler_queue = Queue()
        self.cashier_queue = Queue()
        self.fryer_queue = Queue()
        self.mixer_queue = Queue()
        self.topping_queue = Queue()

        self.assembler_handle = Queue()
        self.boiler_handle = Queue()
        self.cashier_handle = Queue()
        self.fryer_handle = Queue()
        self.mixer_handle = Queue()
        self.topping_handle = Queue()

        self.assembler = Assembler(env)
        self.boiler = Boiler(env)
        self.cashier = Cashier(env)
        self.fryer = Fryer(env)
        self.mixer = Mixer(env)
        self.topping = Topping(env)

    def __store(self):
        """Store data every minute into csv file"""

        while True:
            monitor(self)

            self.csv_writer_per_minute.writerow(
                {
                    "cashier": self.cashier.utilization,
                    "boiler": self.boiler.utilization,
                    "fryer": self.fryer.utilization,
                    "mixer": self.mixer.utilization,
                    "topping": self.topping.utilization,
                    "assembler": self.assembler.utilization,
                    "num_arrivals": self.num_arrivals,
                }
            )

            if self.num_finished_orders == config.MAX_ARRIVALS:
                sys.exit()

            time.sleep(1 * config.SIMULATION_FACTOR)

    def __done(self, order: Order):
        self.num_finished_orders += 1
        self.csv_writer_customer.writerow(
            {
                "name": order.name,
                "quantity": order.quantity,
                "arrival_time": order.arrival_time,
                "being_served_time": order.being_served_time,
                "served_time": order.served_time,
            }
        )

    def run(self):
        """Run the simulation"""

        threading.Thread(target=self.__store).start()

        while True:
            # Generate arrivals.
            yield self.env.timeout(
                random.uniform(
                    config.ARRIVAL_RATE - (config.ARRIVAL_RATE * 25 / 100),
                    config.ARRIVAL_RATE + (config.ARRIVAL_RATE * 25 / 100),
                )
            )

            # Make an order.
            self.num_arrivals += 1
            order = Order(
                self.env,
                self,
                name=self.num_arrivals,
                quantity=random.randint(config.MIN_ORDER_QUANTITY, config.MAX_ORDER_QUANTITY),
                on_complete=self.__done,
            )

            # Add order to queue.
            self.orders.append(order)
            # Process the order.
            self.env.process(order.handle())

            # Stop when the number of arrivals equal to the max arrival.
            if self.num_arrivals == config.MAX_ARRIVALS:
                break
