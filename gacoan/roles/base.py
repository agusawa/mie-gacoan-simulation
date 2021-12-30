import random
import simpy


class Role:
    """
    Base role class.
    """

    def __init__(self, env: simpy.Environment, capacity: int, time: float) -> None:
        self.env = env
        self.capacity = capacity
        self.time = time
        self.resource = simpy.Resource(env, capacity=capacity)
        self.work_time = 0

    def handle(self):
        """Handle customer order"""
        start_work = self.env.now
        yield self.env.timeout(
            random.uniform(
                self.time - (self.time * 15 / 100),
                self.time + (self.time * 15 / 100),
            )
        )
        end_work = self.env.now

        self.work_time += end_work - start_work

    @property
    def utilization(self) -> float:
        """Get utilization value of this role"""
        if self.work_time == 0:
            return 0

        return (self.work_time / self.capacity) / self.env.now
