from typing import List

from ..repositories.models import Size
from ..test.fixtures.size import size_mock


class SizeGenerator:
    def __init__(self) -> None:
        self.sizes: List = None

    def generate(self):
        if not self.sizes:
            self.sizes = []
            for _ in range(5):
                size = size_mock()
                self.sizes.append(size)

        return self.sizes


class SizeSeeder:
    def __init__(self, db=None):
        self.db = db

    def run(self):
        serialized_sizes = SizeGenerator().generate()
        sizes = []
        for size in serialized_sizes:
            current_size = Size(**size)
            self.db.session.add(current_size)
            sizes.append(current_size)
        self.db.session.flush()
        return sizes
