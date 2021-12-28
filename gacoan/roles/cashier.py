import simpy

from gacoan import config
from gacoan.roles import Role


class Cashier(Role):
    """
    Role yang bertugas untuk menangani pemesanan dan pembayaran.
    """

    def __init__(self, env: simpy.RealtimeEnvironment) -> None:
        super().__init__(env, config.CASHIER_CAPACITY, config.CASHIER_TIME)
