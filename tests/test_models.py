# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
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

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db, DataValidationError
from service import app
from tests.factories import ProductFactory
import nose

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def create_and_validate_product(self):
        product = ProductFactory()
        product.id = None
        product.create()
        return product

    def validate_product(self, product):
        "It should validate all fields of product once factory is created"
        self.assertIsNotNone(product.id)
        self.assertIsNotNone(product.name)
        self.assertIsNotNone(product.description)
        self.assertIsNotNone(product.available)
        self.assertIsNotNone(product.price)
        self.assertIsNotNone(product.category)
    
    def validate_serialized_deserialized(self,product,product_dictionary):
        self.assertEqual(product.id, product_dictionary["id"])
        self.assertEqual(product.name, product_dictionary["name"])
        self.assertEqual(product.description, product_dictionary["description"])
        self.assertEqual(str(product.price), str(product_dictionary["price"]))
        self.assertEqual(product.available, product_dictionary["available"])
        self.assertEqual(product.category.name, product_dictionary["category"])


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #
    def test_read_a_product(self):
        """It should read a product from the database"""
        # create a product
        product = ProductFactory()
        # add a log message displaying the product for debugging errors
        logging.info("Product details: " + str(product.serialize()))
        # to assure that id is auto-generated, setting the id to none before record is created
        product.id = None
        
        # after creation, id is auto-generated therefore not none
        product.create()
        self.assertIsNotNone(product.id)

        # fetch the product back from the database
        products = Product.all()
        new_product = products[0]

        self.assertEqual(product.name, new_product.name)
        self.assertEqual(product.description, new_product.description)
        self.assertEqual(product.price, new_product.price)
        self.assertEqual(product.available, new_product.available)
        self.assertEqual(product.category, new_product.category)


    def test_update_a_product(self):
        """It should Update a Product"""
        product = self.create_and_validate_product()

        # Change it an save it
        product.description = "testing"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "testing")
        
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "testing")

        # update again with empty id
        # products[0].id = None

        # """It should update a product from a database"""
        # product = ProductFactory()
        # logging.info("Product details: " + str(product.serialize()))
        # product.id = None
        # product.create()
        # self.assertIsNotNone(product.id)

        # # fetch newly created product
        # products = Product.all()
        # new_product = products[0]

        # # updated
        # logging.info("Before updating:" + str(new_product.serialize()))
        # new_product.description = "updated"
        # original_id = new_product.id
        # new_product.update()
        # self.assertEqual(product.id, original_id)
        # self.assertEqual(product.description,"updated")

        # # Fetch it back and make sure the id has not changed
        # # but the data did change
        # products = Product.all()
        # self.assertEqual(len(products),1)
        # self.assertEqual(products[0].id, original_id)
        # self.assertEqual(products[0].description, "updated")

    def test_update_a_product_empty_id(self):
        """It should raise DataValidationError when Id is empty"""
        # create a product
        product = self.create_and_validate_product()

        # update the product
        product.description = "updated"
        with self.assertRaises(DataValidationError): 
            product.id = None
            product.update()
        # self.assertEqual(str(context.exception),"Update called with empty ID field")



    def test_delete_a_product(self):
       """It should delete a product from a database"""
       # create a product
       product = self.create_and_validate_product()
       
       
       # assert that after creating a product and saving to the database
       # there is only one product in the system
       products = Product.all()
       self.assertEqual(len(products),1)

       # remove product from the database
       product.delete()
       products = Product.all()
       self.assertEqual(len(products),0)

    def test_list_all_products(self):
        """It should list all products"""
        products = Product.all()
        self.assertEqual(len(products),0)

        # create 5 records
        for i in range(5):
            new_product = ProductFactory()
            new_product.create()
        
        products = Product.all()
        self.assertEqual(len(products),5)
    
    def test_find_product_by_name(self):
        """It should find product by name"""
        # # create 5 records
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()

        # retrieve the name of the first product list
        first_product_name = products[0].name

        # count the number of occurrences of the product name in the list
        occurrences = len([product for product in products if product.name == first_product_name])
        
        # retrieve products from the database that have the specified name
        found = Product.find_by_name(first_product_name)

        # assert if the count of the found products matches the expected count
        self.assertEqual(found.count(),occurrences)

        # assert that each product's name matches the expected name
        for product in found: 
            self.assertEqual(product.name, first_product_name)

    
    def test_find_product_by_availability(self):
        """It should find product by availability"""
        # create records
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()

        availability = products[0].available
        count = len([product for product in products if product.available == availability])
        found = Product.find_by_availability(availability)
        self.assertEqual(found.count(), count)

        for product in found:
            self.assertEqual(product.available, availability)

    def test_find_product_by_category(self):
        """It should find product by category"""
        # create products
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)

        # check the number of occurrences
        self.assertEqual(found.count(), count)

        # check if category for found and count is really the same
        for product in found:
            self.assertEqual(product.category, category)

    def test_serialize_product_to_dict(self):
        "It should serialize a product to dictionary"
        # create a product
        product = self.create_and_validate_product()

        product_dictionary = product.serialize()
        self.assertEqual(product.id, product_dictionary["id"])
        self.assertEqual(product.name, product_dictionary["name"])
        self.assertEqual(product.description, product_dictionary["description"])
        self.assertEqual(str(product.price), str(product_dictionary["price"]))
        self.assertEqual(product.available, product_dictionary["available"])
        self.assertEqual(product.category.name, product_dictionary["category"])


    def test_deserialize(self):
        """It should deserialize the dictionary to product object"""
        # create a product
        product = self.create_and_validate_product()

        product_dictionary = product.serialize()
        self.validate_serialized_deserialized(product, product_dictionary)

        product.deserialize(product_dictionary)
        self.validate_serialized_deserialized(product, product_dictionary)
        

    def test_deserialize_available_not_bool(self):
        """It should throw an exception if available is not bool"""
        # create a product
        product = self.create_and_validate_product()

        product_dictionary = product.serialize()
        self.validate_serialized_deserialized(product, product_dictionary)

        # deserialize with wrong available value     
        product_dictionary["available"] = "yes"

        with self.assertRaises(DataValidationError): 
            product.deserialize(product_dictionary)

    









