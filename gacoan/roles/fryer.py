import simpy

from gacoan import config
from gacoan.roles import Role


class Fryer(Role):
    """
    Role in charge of handling noodle frying.
    """

    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env, config.FRYER_CAPACITY, config.FRYER_TIME)
