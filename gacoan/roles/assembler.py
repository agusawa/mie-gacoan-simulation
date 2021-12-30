import simpy

from gacoan import config
from gacoan.roles import Role


class Assembler(Role):
    """
    Role in charge of handling packing orders.
    """

    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env, config.ASSEMBLER_CAPACITY, config.ASSEMBLER_TIME)
