"""
Gacoan Simulation
"""

import os
import random
import simpy
from typing import Callable
from tabulate import tabulate

from gacoan import config
from gacoan.utils import debounce
from gacoan.roles import Assembler, Boiler, Cashier, Fryer, Mixer, Topping


class Queue(object):
    def __init__(self, on_change: Callable[[], None]) -> None:
        self.list = []
        self.on_change = on_change

    def add(self, name: int) -> None:
        if name not in self.list:
            self.list.append(name)
            self.on_change()

    def done(self, name: int) -> None:
        if name in self.list:
            self.list.remove(name)
            self.on_change()


class Gacoan(object):
    def __init__(self, env: simpy.RealtimeEnvironment) -> None:
        self.env: simpy.RealtimeEnvironment = env

        make_queue = lambda: Queue(on_change=lambda: monitor(self))

        self.assembler_queue = make_queue()
        self.assembler_handle = make_queue()

        self.boiler_queue = make_queue()
        self.boiler_handle = make_queue()

        self.cashier_queue = make_queue()
        self.cashier_handle = make_queue()

        self.fryer_queue = make_queue()
        self.fryer_handle = make_queue()

        self.mixer_queue = make_queue()
        self.mixer_handle = make_queue()

        self.topping_queue = make_queue()
        self.topping_handle = make_queue()

        self.assembler = Assembler(env)
        self.boiler = Boiler(env)
        self.cashier = Cashier(env)
        self.fryer = Fryer(env)
        self.mixer = Mixer(env)
        self.topping = Topping(env)

        self.num_arrivals = 0
        self.num_finished_orders = 0

    def run(self):
        while True:
            yield self.env.timeout(
                random.uniform(
                    config.ARRIVAL_RATE - (config.ARRIVAL_RATE * 25 / 100),
                    config.ARRIVAL_RATE + (config.ARRIVAL_RATE * 25 / 100),
                )
            )

            self.num_arrivals += 1
            order = Order(
                self,
                name=self.num_arrivals,
                quantity=random.randint(config.MIN_ORDER_QUANTITY, config.MAX_ORDER_QUANTITY),
            )

            self.env.process(order.handle())

            if self.num_arrivals >= config.MAX_ARRIVALS:
                break


class Order(object):
    def __init__(self, gacoan: Gacoan, name: int, quantity: int) -> None:
        self.env = gacoan.env
        self.gacoan = gacoan

        self.name = name
        self.quantity = quantity

        self.evt_needs_boiled = self.env.event()
        self.evt_needs_fry = self.env.event()
        self.evt_needs_mix = self.env.event()
        self.evt_needs_topping = self.env.event()
        self.evt_needs_assemble = self.env.event()
        self.evt_order_done = self.env.event()

        self.boiler_proc = self.env.process(self.handle_boiler())
        self.fryer_proc = self.env.process(self.handle_fryer())
        self.mixer_proc = self.env.process(self.handle_mixer())
        self.topping_proc = self.env.process(self.handle_topping())
        self.assembler_proc = self.env.process(self.handle_assembler())

        self.env.process(self.done())

    def handle(self):
        return self.handle_cashier()

    def handle_cashier(self):
        self.gacoan.cashier_queue.add(self.name)

        with self.gacoan.cashier.resource.request() as request:
            yield request

            self.gacoan.cashier_queue.done(self.name)

            self.gacoan.cashier_handle.add(self.name)
            yield self.env.process(self.gacoan.cashier.handle())
            self.gacoan.cashier_handle.done(self.name)

            self.evt_needs_boiled.succeed()
            self.evt_needs_boiled = self.env.event()

    def handle_boiler(self):
        yield self.evt_needs_boiled

        self.gacoan.boiler_queue.add(self.name)

        with self.gacoan.boiler.resource.request() as request:
            for i in range(self.quantity):
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

    def handle_fryer(self):
        i = yield self.evt_needs_fry
        self.fryer_proc = self.env.process(self.handle_fryer())

        self.gacoan.fryer_queue.add(self.name)

        with self.gacoan.fryer.resource.request() as request:
            yield request

            self.gacoan.fryer_queue.done(self.name)

            self.gacoan.fryer_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.fryer.handle())
            self.gacoan.fryer_handle.done(f"{self.name}[{i + 1}]")

            self.evt_needs_mix.succeed(i)
            self.evt_needs_mix = self.env.event()

    def handle_mixer(self):
        i = yield self.evt_needs_mix
        self.mixer_proc = self.env.process(self.handle_mixer())

        self.gacoan.mixer_queue.add(self.name)

        with self.gacoan.mixer.resource.request() as request:
            yield request

            self.gacoan.mixer_queue.done(self.name)

            self.gacoan.mixer_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.mixer.handle())
            self.gacoan.mixer_handle.done(f"{self.name}[{i + 1}]")

            self.evt_needs_topping.succeed(i)
            self.evt_needs_topping = self.env.event()

    def handle_topping(self):
        i = yield self.evt_needs_topping
        self.topping_proc = self.env.process(self.handle_topping())

        self.gacoan.topping_queue.add(self.name)

        with self.gacoan.topping.resource.request() as request:
            yield request

            self.gacoan.topping_queue.done(self.name)

            self.gacoan.topping_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.topping.handle())
            self.gacoan.topping_handle.done(f"{self.name}[{i + 1}]")

            self.evt_needs_assemble.succeed(i)
            self.evt_needs_assemble = self.env.event()

    def handle_assembler(self):
        i = yield self.evt_needs_assemble
        self.assembler_proc = self.env.process(self.handle_assembler())

        self.gacoan.assembler_queue.add(self.name)

        with self.gacoan.assembler.resource.request() as request:
            yield request

            self.gacoan.assembler_queue.done(self.name)

            self.gacoan.assembler_handle.add(f"{self.name}[{i + 1}]")
            yield self.env.process(self.gacoan.assembler.handle())
            self.gacoan.assembler_handle.done(f"{self.name}[{i + 1}]")

            self.evt_order_done.succeed(i)
            self.evt_order_done = self.env.event()

    def done(self):
        for i in range(self.quantity):
            yield self.evt_order_done

            monitor(self.gacoan)

            if i + 1 == self.quantity:
                self.gacoan.num_finished_orders += 1


@debounce(0.05)
def monitor(gacoan: Gacoan):
    def short_list(data: list):
        if len(data) > 6:
            newList = data[:6]
            newList.append("...")
            return newList
        return data

    if config.MONITORING_MODE:
        os.system("clear")

        print(f"Menit : {int(gacoan.env.now)}")
        print("")

        print(f"Jumlah Kedatangan : {gacoan.num_arrivals}")
        print(f"Jumlah Order Selesai : {gacoan.num_finished_orders}")
        print("")

        print(
            tabulate(
                [
                    [
                        f"[{len(gacoan.cashier_queue.list)}]",
                        "Dalam Antrian",
                        short_list(gacoan.cashier_queue.list),
                    ],
                    [
                        f"[{len(gacoan.cashier_handle.list)}]",
                        "Dilayani Kasir",
                        short_list(gacoan.cashier_handle.list),
                    ],
                    ["", "", ""],
                    [
                        f"[{len(gacoan.boiler_queue.list)}]",
                        "Menuggu Perebusan Mie",
                        short_list(gacoan.boiler_queue.list),
                    ],
                    [
                        f"[{len(gacoan.boiler_handle.list)}]",
                        "Mie Direbus",
                        short_list(gacoan.boiler_handle.list),
                    ],
                    ["", "", ""],
                    [
                        f"[{len(gacoan.fryer_queue.list)}]",
                        "Menuggu Penggorengan Mie",
                        short_list(gacoan.fryer_queue.list),
                    ],
                    [
                        f"[{len(gacoan.fryer_handle.list)}]",
                        "Mie Digoreng",
                        short_list(gacoan.fryer_handle.list),
                    ],
                    ["", "", ""],
                    [
                        f"[{len(gacoan.mixer_queue.list)}]",
                        "Menuggu Pengadukan Mie",
                        short_list(gacoan.mixer_queue.list),
                    ],
                    [
                        f"[{len(gacoan.mixer_handle.list)}]",
                        "Mie Diaduk",
                        short_list(gacoan.mixer_handle.list),
                    ],
                    ["", "", ""],
                    [
                        f"[{len(gacoan.topping_queue.list)}]",
                        "Menuggu Pemberian Topping",
                        short_list(gacoan.topping_queue.list),
                    ],
                    [
                        f"[{len(gacoan.topping_handle.list)}]",
                        "Mie Diberikan Topping",
                        short_list(gacoan.topping_handle.list),
                    ],
                    ["", "", ""],
                    [
                        f"[{len(gacoan.assembler_queue.list)}]",
                        "Menuggu Assembler",
                        short_list(gacoan.assembler_queue.list),
                    ],
                    [
                        f"[{len(gacoan.assembler_handle.list)}]",
                        "Dilayani Assembler",
                        short_list(gacoan.assembler_handle.list),
                    ],
                ]
            )
        )

        print("\nUtilization")
        print(
            tabulate(
                [
                    ["Kasir", gacoan.cashier.utilization],
                    ["Perebus Mie", gacoan.boiler.utilization],
                    ["Penggoreng Mie", gacoan.fryer.utilization],
                    ["Pengaduk", gacoan.mixer.utilization],
                    ["Pemberi Topping", gacoan.topping.utilization],
                    ["Assembler", gacoan.assembler.utilization],
                ]
            )
        )
