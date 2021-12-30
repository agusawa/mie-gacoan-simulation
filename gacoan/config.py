"""
Configuration
"""

REALTIME_MODE: bool = True
MONITORING_MODE: bool = True
SIMULATION_TIME: int = 240  # In minutes
SIMULATION_FACTOR: float = 0.1

ARRIVAL_RATE: float = 0.630  # In minutes
MAX_ARRIVALS: int = 154

MIN_ORDER_QUANTITY: int = 1
MAX_ORDER_QUANTITY: int = 4

"""Role capacity"""
CASHIER_CAPACITY: int = 1
BOILER_CAPACITY: int = 6
FRYER_CAPACITY: int = 3
MIXER_CAPACITY: int = 1
TOPPING_CAPACITY: int = 1
ASSEMBLER_CAPACITY: int = 1

"""Service Time (in minutes)"""
CASHIER_TIME: float = 0.716
BOILER_TIME: float = 3
FRYER_TIME: float = 2
MIXER_TIME: float = 0.25
TOPPING_TIME: float = 0.25
ASSEMBLER_TIME: float = 0.25

"""CSV"""
CSV_FILE_PER_MINUTE_RESULT: str = "per-minute.csv"
CSV_FILE_CUSTOMER_RESULT: str = "customer.csv"
