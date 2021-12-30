import random
from typing import Callable
from typing_extensions import Self

import simpy


class Order:
    """Customer's order class"""

    env: simpy.Environment
    gacoan: None

    name: int
    quantity: int
    on_complete: Callable[[Self], None]

    # Timeline
    arrival_time: float
    being_served_time: float
    served_time: float

    time_cashier: float
    time_boiler: float
    time_fryer: float
    time_mixer: float
    time_topping: float
    time_assembler: float

    time_cashier: float
    time_boiler: float
    time_fryer: float
    time_mixer: float
    time_topping: float
    time_assembler: float

    # Simpy events
    evt_needs_boiled: simpy.Event
    evt_needs_fry: simpy.Event
    evt_needs_mix: simpy.Event
    evt_needs_topping: simpy.Event
    evt_needs_assemble: simpy.Event
    evt_order_done: simpy.Event

    # Simpy processes
    boiler_proc: simpy.Process
    fryer_proc: simpy.Process
    mixer_proc: simpy.Process
    topping_proc: simpy.Process
    assembler_proc: simpy.Process

    def __init__(
        self,
        env: simpy.Environment,
        gacoan,
        name: int,
        quantity: int,
        on_complete: Callable[[Self], None],
    ) -> None:
        self.env = env
        self.gacoan = gacoan

        self.name = name
        self.quantity = quantity
        self.on_complete = on_complete

        self.evt_needs_boiled = self.env.event()
        self.evt_needs_fry = self.env.event()
        self.evt_needs_mix = self.env.event()
        self.evt_needs_topping = self.env.event()
        self.evt_needs_assemble = self.env.event()
        self.evt_order_done = self.env.event()

        self.boiler_proc = self.env.process(self.__handle_boiler())
        self.fryer_proc = self.env.process(self.__handle_fryer())
        self.mixer_proc = self.env.process(self.__handle_mixer())
        self.topping_proc = self.env.process(self.__handle_topping())
        self.assembler_proc = self.env.process(self.__handle_assembler())

        self.arrival_time = self.env.now

        self.env.process(self.__done())

    def handle(self):
        """Add customer orders into simulation for processing"""
        return self.__handle_cashier()

    def __handle_cashier(self):
        self.gacoan.cashier_queue.add(self.name)

        with self.gacoan.cashier.resource.request() as request:
            yield request

            self.being_served_time = self.env.now
            self.gacoan.cashier_queue.done(self.name)

            self.gacoan.cashier_handle.add(self.name)
            yield self.env.process(self.gacoan.cashier.handle())
            self.gacoan.cashier_handle.done(self.name)

            self.evt_needs_boiled.succeed()
            self.evt_needs_boiled = self.env.event()

    def __handle_boiler(self):
        yield self.evt_needs_boiled

        self.gacoan.boiler_queue.add(self.name)

        def handle(i: int):
            with self.gacoan.boiler.resource.request() as request:
                yield request

                self.gacoan.boiler_queue.done(self.name)

                self.gacoan.boiler_handle.add(f"{self.name}[{i + 1}]")
                yield self.env.process(self.gacoan.boiler.handle())
                self.gacoan.boiler_handle.done(f"{self.name}[{i + 1}]")

                if random.randint(0, 1) == 1:
                    self.evt_needs_fry.succeed(i)
                    self.evt_needs_fry = self.env.event()
                else:
                    self.evt_needs_mix.succeed(i)
                    self.evt_needs_mix = self.env.event()

        for i in range(self.quantity):
            self.env.process(handle(i))

    def __handle_fryer(self):
        i = yield self.evt_needs_fry
        self.fryer_proc = self.env.process(self.__handle_fryer())

        self.gacoan.fryer_queue.add(self.name)

        with self.gacoan.fryer.resource.request() as request:
            yield request

            self.gacoan.fryer_queue.done(self.name)

            self.gacoan.fryer_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.fryer.handle())
            self.gacoan.fryer_handle.done(f"{self.name}[{i + 1}]")

            self.evt_needs_mix.succeed(i)
            self.evt_needs_mix = self.env.event()

    def __handle_mixer(self):
        i = yield self.evt_needs_mix
        self.mixer_proc = self.env.process(self.__handle_mixer())

        self.gacoan.mixer_queue.add(self.name)

        with self.gacoan.mixer.resource.request() as request:
            yield request

            self.gacoan.mixer_queue.done(self.name)

            self.gacoan.mixer_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.mixer.handle())
            self.gacoan.mixer_handle.done(f"{self.name}[{i + 1}]")

            self.evt_needs_topping.succeed(i)
            self.evt_needs_topping = self.env.event()

    def __handle_topping(self):
        i = yield self.evt_needs_topping
        self.topping_proc = self.env.process(self.__handle_topping())

        self.gacoan.topping_queue.add(self.name)

        with self.gacoan.topping.resource.request() as request:
            yield request

            self.gacoan.topping_queue.done(self.name)

            self.gacoan.topping_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.topping.handle())
            self.gacoan.topping_handle.done(f"{self.name}[{i + 1}]")

            self.evt_needs_assemble.succeed(i)
            self.evt_needs_assemble = self.env.event()

    def __handle_assembler(self):
        i = yield self.evt_needs_assemble
        self.assembler_proc = self.env.process(self.__handle_assembler())

        self.gacoan.assembler_queue.add(self.name)

        with self.gacoan.assembler.resource.request() as request:
            yield request

            self.gacoan.assembler_queue.done(self.name)

            self.gacoan.assembler_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.assembler.handle())
            self.gacoan.assembler_handle.done(f"{self.name}[{i + 1}]")

            self.evt_order_done.succeed(i)
            self.evt_order_done = self.env.event()

    def __done(self):
        for i in range(self.quantity):
            yield self.evt_order_done

            if i + 1 == self.quantity:
                self.served_time = self.env.now
                self.on_complete(self)
