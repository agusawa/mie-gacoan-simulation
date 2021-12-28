import simpy

from gacoan import config
from gacoan.roles import Role


class Topping(Role):
    """
    Role yang bertugas untuk menangani pemberian topping.
    """

    def __init__(self, env: simpy.RealtimeEnvironment) -> None:
        super().__init__(env, config.TOPPING_CAPACITY, config.TOPPING_TIME)
