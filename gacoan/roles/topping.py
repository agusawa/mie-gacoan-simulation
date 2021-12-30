import simpy

from gacoan import config
from gacoan.roles import Role


class Topping(Role):
    """
    Role in charge of handling the topping.
    """

    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env, config.TOPPING_CAPACITY, config.TOPPING_TIME)
