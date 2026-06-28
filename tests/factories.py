"""
Test Factory to make fake objects for testing
"""
from datetime import date
import factory
from factory.fuzzy import FuzzyDate
from service.models import Account


class AccountFactory(factory.Factory):
    """Creates fake Accounts"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Persistent class"""

        model = Account

    id = factory.Sequence(lambda n: n)  # pylint: disable=invalid-name
    name = factory.Faker("name")
    email = factory.Faker("email")
    address = factory.Faker("address")
    phone_number = factory.Faker("phone_number")
    date_joined = FuzzyDate(date(2008, 1, 1))
