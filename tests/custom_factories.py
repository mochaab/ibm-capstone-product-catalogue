"""
AccountFactory class using FactoryBoy

Documentation on Faker Providers:
    https://faker.readthedocs.io/en/master/providers/baseprovider.html

Documentation on Fuzzy Attributes:
    https://factoryboy.readthedocs.io/en/stable/fuzzy.html

"""
import random

# from factory.fuzzy import FuzzyChoice, FuzzyDate

class CustomFactory():
    """ Creates fake Accounts """
    
    def random_choice(types) -> list:
        return random.choice(types)