import simpy

from gacoan import config
from gacoan.roles import Role


class Mixer(Role):
    """
    Role yang bertugas untuk menangani pengaudukan mie dengan bumbu.
    """

    def __init__(self, env: simpy.RealtimeEnvironment) -> None:
        super().__init__(env, config.MIXER_CAPACITY, config.MIXER_TIME)
