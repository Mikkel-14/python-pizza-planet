from typing import List

from ..repositories.models import Ingredient
from ..test.fixtures.ingredient import ingredient_mock


class IngredientGenerator:
    def __init__(self) -> None:
        self.ingredients: List = None

    def generate(self):
        if not self.ingredients:
            self.ingredients = []
            for _ in range(10):
                ingredient = ingredient_mock()
                self.ingredients.append(ingredient)

        return self.ingredients


class IngredientSeeder:
    def __init__(self, db=None):
        self.db = db

    def run(self):
        serialized_ingredients = IngredientGenerator().generate()
        ingredients = []
        for ingredient in serialized_ingredients:
            current_ingredient = Ingredient(**ingredient)
            self.db.session.add(current_ingredient)
            ingredients.append(current_ingredient)
        self.db.session.flush()
        return ingredients
