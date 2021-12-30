import os
from threading import Timer
from typing import Any, Callable

from tabulate import tabulate

from gacoan import config


def debounce(wait: float):
    """Debounce function"""

    def decorator(callback: Callable[[Any], Any]):
        def debounced(*args, **kwargs):
            def call_it():
                callback(*args, **kwargs)

            try:
                debounced.t.cancel()
            except AttributeError:
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()

        return debounced

    return decorator


@debounce(0.05)
def monitor(gacoan):
    """Show simulation info"""

    # Only show information when monitoring mode is True
    if not config.MONITORING_MODE:
        return

    def shorten_list(data: list, max_index: int = 6):
        """Make list more shorten"""
        if len(data) > max_index:
            new_data = data[:max_index]
            new_data.append("...")
            return new_data
        return data

    os.system("cls" if os.name == "nt" else "clear")

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
                    shorten_list(gacoan.cashier_queue.list),
                ],
                [
                    f"[{len(gacoan.cashier_handle.list)}]",
                    "Dilayani Kasir",
                    shorten_list(gacoan.cashier_handle.list),
                ],
                ["", "", ""],
                [
                    f"[{len(gacoan.boiler_queue.list)}]",
                    "Menuggu Perebusan Mie",
                    shorten_list(gacoan.boiler_queue.list),
                ],
                [
                    f"[{len(gacoan.boiler_handle.list)}]",
                    "Mie Direbus",
                    shorten_list(gacoan.boiler_handle.list),
                ],
                ["", "", ""],
                [
                    f"[{len(gacoan.fryer_queue.list)}]",
                    "Menuggu Penggorengan Mie",
                    shorten_list(gacoan.fryer_queue.list),
                ],
                [
                    f"[{len(gacoan.fryer_handle.list)}]",
                    "Mie Digoreng",
                    shorten_list(gacoan.fryer_handle.list),
                ],
                ["", "", ""],
                [
                    f"[{len(gacoan.mixer_queue.list)}]",
                    "Menuggu Pengadukan Mie",
                    shorten_list(gacoan.mixer_queue.list),
                ],
                [
                    f"[{len(gacoan.mixer_handle.list)}]",
                    "Mie Diaduk",
                    shorten_list(gacoan.mixer_handle.list),
                ],
                ["", "", ""],
                [
                    f"[{len(gacoan.topping_queue.list)}]",
                    "Menuggu Pemberian Topping",
                    shorten_list(gacoan.topping_queue.list),
                ],
                [
                    f"[{len(gacoan.topping_handle.list)}]",
                    "Mie Diberikan Topping",
                    shorten_list(gacoan.topping_handle.list),
                ],
                ["", "", ""],
                [
                    f"[{len(gacoan.assembler_queue.list)}]",
                    "Menuggu Assembler",
                    shorten_list(gacoan.assembler_queue.list),
                ],
                [
                    f"[{len(gacoan.assembler_handle.list)}]",
                    "Dilayani Assembler",
                    shorten_list(gacoan.assembler_handle.list),
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
