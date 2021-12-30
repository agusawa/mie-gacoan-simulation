import simpy

from gacoan import config
from gacoan.roles import Role


class Boiler(Role):
    """
    Role in charge of handling the boiling of noodles.
    """

    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env, config.BOILER_CAPACITY, config.BOILER_TIME)
