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

    simulation = Gacoan(env)

    env.process(simulation.run())
    env.run(until=config.SIMULATION_TIME)
