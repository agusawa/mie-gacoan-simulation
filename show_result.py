import csv

import matplotlib.pyplot as plt
import numpy as np

from gacoan import config


fig, axs = plt.subplots(3, 2, constrained_layout=True)

fig.canvas.set_window_title("Mie Gacoan Simulation Result")

utilities: plt.Axes = axs[0][0]
utilities_avg: plt.Axes = axs[1][0]
utilities_bar: plt.Axes = axs[2][0]

num_customers: plt.Axes = axs[0][1]
lead_time: plt.Axes = axs[1][1]
flow_time: plt.Axes = axs[2][1]


data = {
    "utilization": {
        "cashier": [],
        "boiler": [],
        "fryer": [],
        "mixer": [],
        "topping": [],
        "assembler": [],
    },
    "average_utilization": [],
    "num_arrivals": [],
    "lead_time": [],
    "flow_time": [],
}


with open(f"./output/{config.CSV_FILE_PER_MINUTE_RESULT}", newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    for j, row in enumerate(reader):
        data["utilization"]["cashier"].append(float(row["cashier"]))
        data["utilization"]["boiler"].append(float(row["boiler"]))
        data["utilization"]["fryer"].append(float(row["fryer"]))
        data["utilization"]["mixer"].append(float(row["mixer"]))
        data["utilization"]["topping"].append(float(row["topping"]))
        data["utilization"]["assembler"].append(float(row["assembler"]))

        data["average_utilization"].append(
            (
                float(row["cashier"])
                + float(row["boiler"])
                + float(row["fryer"])
                + float(row["mixer"])
                + float(row["topping"])
                + float(row["assembler"])
            )
            / 6
        )

        data["num_arrivals"].append(float(row["num_arrivals"]))

with open(f"./output/{config.CSV_FILE_CUSTOMER_RESULT}", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for j, row in enumerate(reader):
        data["lead_time"].append(float(row["served_time"]) - float(row["arrival_time"]))
        data["flow_time"].append(float(row["served_time"]) - float(row["being_served_time"]))

utilities_x = [i for i in range(len(data["utilization"]["cashier"]))]
utilities.grid()
utilities.set_title("Utilitas")
utilities.set_xlabel("Menit")
utilities.set_ylabel("Utilitas")
utilities.set_ylim([0, 1])
utilities.plot(utilities_x, data["utilization"]["cashier"], "tab:blue", linewidth=1, label="Kasir")
utilities.plot(
    utilities_x, data["utilization"]["boiler"], "tab:orange", linewidth=1, label="Perebus"
)
utilities.plot(
    utilities_x, data["utilization"]["fryer"], "tab:green", linewidth=1, label="Penggoreng"
)
utilities.plot(utilities_x, data["utilization"]["mixer"], "tab:red", linewidth=1, label="Pengaduk")
utilities.plot(
    utilities_x, data["utilization"]["topping"], "tab:purple", linewidth=1, label="Pemberi Topping"
)
utilities.plot(
    utilities_x, data["utilization"]["assembler"], "tab:brown", linewidth=1, label="Assembler"
)
utilities.legend(loc="upper left", bbox_to_anchor=(1, 1))


utilities_avg.grid()
utilities_avg.set_title("Rata-rata Utilitas")
utilities_avg.set_xlabel("Menit")
utilities_avg.set_ylabel("Rata-rata")
utilities_avg.set_ylim([0, 1])
utilities_avg.plot(
    utilities_x, data["average_utilization"], "tab:orange", linewidth=1, label="Pelanggan"
)


utilities_bar.grid(axis="x")
utilities_bar.set_title("Utilitas Bagian")
utilities_bar.set_xlabel("Utilitas")
utilities_bar.set_xlim([0, 1])
utilities_bar.barh(
    ["Kasir", "Perebus", "Penggoreng", "Pengaduk", "Pemberi\nTopping", "Assembler"],
    [
        np.mean(data["utilization"]["cashier"]),
        np.mean(data["utilization"]["boiler"]),
        np.mean(data["utilization"]["fryer"]),
        np.mean(data["utilization"]["mixer"]),
        np.mean(data["utilization"]["topping"]),
        np.mean(data["utilization"]["assembler"]),
    ],
)


num_customers.grid()
num_customers.set_title("Kedatangan Pelanggan")
num_customers.set_xlabel("Menit")
num_customers.set_ylabel("Jumlah Pelanggan")
num_customers.set_ylim([0, config.MAX_ARRIVALS])
num_customers.autoscale(True, axis="x")
num_customers.plot(utilities_x, data["num_arrivals"], "tab:green", linewidth=1, label="Pelanggan")


lead_time.grid()
lead_time.set_title("Lead Time")
lead_time.plot(
    [i for i in range(len(data["lead_time"]))], data["lead_time"], "tab:orange", linewidth=1
)


flow_time.grid()
flow_time.set_title("Flow Time")
flow_time.plot(
    [i for i in range(len(data["flow_time"]))], data["flow_time"], "tab:orange", linewidth=1
)

plt.show()
