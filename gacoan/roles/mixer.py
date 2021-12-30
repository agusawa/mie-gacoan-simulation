import simpy

from gacoan import config
from gacoan.roles import Role


class Mixer(Role):
    """
    Role in charge of handling complaints of noodles with spices.
    """

    def __init__(self, env: simpy.Environment) -> None:
        super().__init__(env, config.MIXER_CAPACITY, config.MIXER_TIME)
