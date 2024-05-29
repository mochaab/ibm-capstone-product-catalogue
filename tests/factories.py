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
import factory
from tests.custom_factories import CustomFactory
from factory.fuzzy import FuzzyDecimal
from service.models import Product, Category

AVAILABILITY = [x for x in [True, False]]
PRODUCT_NAME = [x for x in ["Hat",
                            "Pants",
                            "Shirt",
                            "Apple",
                            "Banana",
                            "Pots",
                            "Towels",
                            "Ford",
                            "Chevy",
                            "Hammer",
                            "Wrench"]]


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    # Add code to create Fake Products
    name = CustomFactory.random_choice(PRODUCT_NAME)
    description = factory.Faker("text")
    price = FuzzyDecimal(0.5, 2000.0, 2)
    available = CustomFactory.random_choice(AVAILABILITY)
    category = CustomFactory.random_choice(
        [Category.UNKNOWN,
         Category.CLOTHS,
         Category.FOOD,
         Category.HOUSEWARES,
         Category.AUTOMOTIVE,
         Category.TOOLS])
