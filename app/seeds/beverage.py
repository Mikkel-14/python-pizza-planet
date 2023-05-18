from typing import List

from ..repositories.models import Beverage
from ..test.fixtures.beverage import beverage_mock


class BeverageGenerator:
    def __init__(self) -> None:
        self.beverages: List = None

    def generate(self):
        if not self.beverages:
            self.beverages = []
            for _ in range(10):
                beverage = beverage_mock()
                self.beverages.append(beverage)

        return self.beverages


class BeverageSeeder:
    def __init__(self, db=None):
        self.db = db

    def run(self):
        serialized_beverages = BeverageGenerator().generate()
        beverages = []
        for beverage in serialized_beverages:
            current_beverage = Beverage(**beverage)
            self.db.session.add(current_beverage)
            beverages.append(current_beverage)
        self.db.session.flush()
        return beverages
