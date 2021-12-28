import random
import simpy

from gacoan import config
from gacoan.roles import Role


class Boiler(Role):
    """
    Role yang bertugas untuk menangani perebusan mie.
    """

    def __init__(self, env: simpy.RealtimeEnvironment) -> None:
        super().__init__(env, config.BOILER_CAPACITY, config.BOILER_TIME)
