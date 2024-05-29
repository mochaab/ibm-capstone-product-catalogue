# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=too-few-public-methods

"""
Test Factory to make fake objects for testing
"""
import random
import factory
from factory.fuzzy import FuzzyDecimal
from service.models import Product, Category

AVAILABILITY = [True, False]
PRODUCT_NAME = ["Hat",
                "Pants",
                "Shirt",
                "Apple",
                "Banana",
                "Pots",
                "Towels",
                "Ford",
                "Chevy",
                "Hammer",
                "Wrench"]


class CustomFactory():
    """ Creates fake Accounts """

    @classmethod
    def random_choice(cls, types) -> list:
        """ This randomly choice a value in the list of types """
        return random.choice(types)


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    # Add code to create Fake Products
    name = CustomFactory.random_choice(types=PRODUCT_NAME)
    description = factory.Faker("text")
    price = FuzzyDecimal(0.5, 2000.0, 2)
    available = CustomFactory.random_choice(types=AVAILABILITY)
    category = CustomFactory.random_choice(
        types=[Category.UNKNOWN,
               Category.CLOTHS,
               Category.FOOD,
               Category.HOUSEWARES,
               Category.AUTOMOTIVE,
               Category.TOOLS])
