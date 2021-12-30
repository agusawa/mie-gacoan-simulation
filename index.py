import csv

import simpy
from tabulate import tabulate

from gacoan import config
from gacoan.app import Gacoan

if __name__ == "__main__":
    print(
        tabulate(
            [
                ["Durasi Simulasi", config.SIMULATION_TIME, "menit"],
                ["Arrival Rate", config.ARRIVAL_RATE, "menit"],
                ["Max Kedatangan", config.MAX_ARRIVALS, "pelanggan"],
                ["Min Order", config.MIN_ORDER_QUANTITY, "qty"],
                ["Max Order", config.MAX_ORDER_QUANTITY, "qty"],
                ["", ""],
                ["Server Kasir", config.CASHIER_CAPACITY, "server"],
                ["Mesin Perebus Mie", config.BOILER_CAPACITY, "kapasitas satu kali rebus"],
                ["Wajan Penggoreng Mie", config.FRYER_CAPACITY, "wajan"],
                ["Pengaduk", config.MIXER_CAPACITY, "pegawai"],
                ["Pemberi Topping", config.TOPPING_CAPACITY, "pegawai"],
                ["Assembler", config.ASSEMBLER_CAPACITY, "pegawai"],
                ["", ""],
                ["Waktu Pelayanan Kasir", config.CASHIER_TIME, "menit"],
                ["Waktu Perebusan Mie", config.BOILER_TIME, "menit"],
                ["Waktu Penggorengan Mie", config.FRYER_TIME, "menit"],
                ["Waktu Mengaduk Mie", config.MIXER_TIME, "menit"],
                ["Waktu Memberi Topping", config.TOPPING_TIME, "menit"],
                ["Waktu Assemble", config.ASSEMBLER_TIME, "menit"],
            ],
            headers=["Nama Variable", "Nilai", "Satuan"],
        )
    )
    input("\n\n[Press ENTER to run]")

    if config.REALTIME_MODE:
        env = simpy.RealtimeEnvironment(factor=config.SIMULATION_FACTOR)
    else:
        env = simpy.Environment()

    CSV_PER_MINUTE_FIELDS = [
        "cashier",
        "boiler",
        "fryer",
        "mixer",
        "topping",
        "assembler",
        "num_arrivals",
    ]

    CSV_CUSTOMER_FIELDS = [
        "name",
        "quantity",
        "arrival_time",
        "being_served_time",
        "served_time",
    ]

    # Insert field names
    with open(
        f"./output/{config.CSV_FILE_PER_MINUTE_RESULT}", "w", newline="", encoding="utf-8"
    ) as csv_file_per_minute, open(
        f"./output/{config.CSV_FILE_CUSTOMER_RESULT}", "w", newline="", encoding="utf-8"
    ) as csv_file_customer:
        csv.DictWriter(csv_file_per_minute, fieldnames=CSV_PER_MINUTE_FIELDS).writeheader()
        csv.DictWriter(csv_file_customer, fieldnames=CSV_CUSTOMER_FIELDS).writeheader()

    # Open csv files and run the simulation
    with open(
        f"./output/{config.CSV_FILE_PER_MINUTE_RESULT}", "a", newline="", encoding="utf-8"
    ) as csv_file_per_minute, open(
        f"./output/{config.CSV_FILE_CUSTOMER_RESULT}", "a", newline="", encoding="utf-8"
    ) as csv_file_customer:
        simulation = Gacoan(
            env,
            csv_writer_per_minute=csv.DictWriter(
                csv_file_per_minute,
                fieldnames=CSV_PER_MINUTE_FIELDS,
            ),
            csv_writer_customer=csv.DictWriter(
                csv_file_customer,
                fieldnames=CSV_CUSTOMER_FIELDS,
            ),
        )

        env.process(simulation.run())
        env.run(until=config.SIMULATION_TIME)
