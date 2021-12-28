import simpy

from gacoan import config
from gacoan.roles import Role


class Fryer(Role):
    """
    Role yang bertugas untuk menangani perebusan mie.
    """

    def __init__(self, env: simpy.RealtimeEnvironment) -> None:
        super().__init__(env, config.FRYER_CAPACITY, config.FRYER_TIME)
