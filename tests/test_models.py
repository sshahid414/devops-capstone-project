"""
Test cases for Account Model

Test cases can be run with:
    nosetests
    coverage report -m
"""
import os
import logging
import unittest
from datetime import date
from service import app
from service.models import Account, DataValidationError, db
from tests.factories import AccountFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///accounts.db"
)


######################################################################
#  Account   M O D E L   T E S T   C A S E S
######################################################################
class TestAccount(unittest.TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        db.session.query(Account).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_account(self):
        """It should Create an Account and assert that it exists"""
        fake_account = AccountFactory()
        account = Account(
            name=fake_account.name,
            email=fake_account.email,
            address=fake_account.address,
            phone_number=fake_account.phone_number,
            date_joined=fake_account.date_joined,
        )
        self.assertIsNotNone(account)
        self.assertEqual(account.id, None)
        self.assertEqual(account.name, fake_account.name)
        self.assertEqual(account.email, fake_account.email)
        self.assertEqual(account.address, fake_account.address)
        self.assertEqual(account.phone_number, fake_account.phone_number)
        self.assertEqual(account.date_joined, fake_account.date_joined)

    def test_add_a_account(self):
        """It should Create an account and add it to the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        account = AccountFactory()
        account.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(account.id)
        accounts = Account.all()
        self.assertEqual(len(accounts), 1)

    def test_read_account(self):
        """It should Read an account"""
        account = AccountFactory()
        account.create()

        # Read it back
        found_account = Account.find(account.id)
        self.assertEqual(found_account.id, account.id)
        self.assertEqual(found_account.name, account.name)
        self.assertEqual(found_account.email, account.email)
        self.assertEqual(found_account.address, account.address)
        self.assertEqual(found_account.phone_number, account.phone_number)
        self.assertEqual(found_account.date_joined, account.date_joined)

    def test_update_account(self):
        """It should Update an account"""
        account = AccountFactory(email="advent@change.me")
        account.create()
        self.assertIsNotNone(account.id)
        # Fetch it back
        account = Account.find(account.id)
        account.email = "XYZZY@plugh.com"
        account.update()
        # Fetch it back again
        account = Account.find(account.id)
        self.assertEqual(account.email, "XYZZY@plugh.com")

    def test_delete_an_account(self):
        """It should Delete an account from the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        account = AccountFactory()
        account.create()
        self.assertEqual(len(Account.all()), 1)
        # delete the account and make sure it isn't in the database
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_list_all_accounts(self):
        """It should List all Accounts in the database"""
        accounts = Account.all()
        self.assertEqual(accounts, [])
        # Create 5 Accounts
        for _ in range(5):
            account = AccountFactory()
            account.create()
        # See if we get back 5 accounts
        accounts = Account.all()
        self.assertEqual(len(accounts), 5)

    def test_find_by_name(self):
        """It should Find an Account by id"""
        account = AccountFactory()
        account.create()
        # Fetch it back by id
        same_account = Account.find(account.id)
        self.assertEqual(same_account.id, account.id)
        self.assertEqual(same_account.name, account.name)

    def test_serialize_an_account(self):
        """It should Serialize an account"""
        account = AccountFactory()
        serial_account = account.serialize()
        self.assertEqual(serial_account["id"], account.id)
        self.assertEqual(serial_account["name"], account.name)
        self.assertEqual(serial_account["email"], account.email)
        self.assertEqual(serial_account["address"], account.address)
        self.assertEqual(serial_account["phone_number"], account.phone_number)
        self.assertEqual(serial_account["date_joined"], str(account.date_joined))

    def test_deserialize_an_account(self):
        """It should Deserialize an account"""
        account = AccountFactory()
        account.create()
        serial_account = account.serialize()
        new_account = Account()
        new_account.deserialize(serial_account)
        self.assertEqual(new_account.name, account.name)
        self.assertEqual(new_account.email, account.email)
        self.assertEqual(new_account.address, account.address)
        self.assertEqual(new_account.phone_number, account.phone_number)
        self.assertEqual(new_account.date_joined, account.date_joined)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an account with a KeyError"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an account with a TypeError"""
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, [])

    def test_deserialize_without_date_joined(self):
        """It should Deserialize an account and default the date_joined"""
        account = AccountFactory()
        serial_account = account.serialize()
        del serial_account["date_joined"]
        new_account = Account()
        new_account.deserialize(serial_account)
        self.assertEqual(new_account.date_joined, date.today())


if __name__ == "__main__":
    unittest.main()
