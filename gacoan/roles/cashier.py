import simpy

from gacoan import config
from gacoan.roles import Role


class Cashier(Role):
    """
    Role in charge of handling orders and payments.
    """

    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env, config.CASHIER_CAPACITY, config.CASHIER_TIME)
