import random
import simpy

from gacoan import config
from gacoan.roles import Role


class Assembler(Role):
    """
    Role yang bertugas untuk menangani packing pesanan.
    """

    def __init__(self, env: simpy.RealtimeEnvironment) -> None:
        super().__init__(env, config.ASSEMBLER_CAPACITY, config.ASSEMBLER_TIME)
