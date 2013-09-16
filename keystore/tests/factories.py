import factory
from keys.models import KeyPair
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    email = 'admin@admin.com'
    username = factory.Sequence(lambda n: 'test_user_{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    is_superuser = False
    is_staff = False
    is_active = True

class KeyPairFactory(factory.Factory):
    FACTORY_FOR = KeyPair
    key_name = factory.Sequence(lambda n: 'Test Key {0}'.format(n))
    key_value = "This is a test value for a test key"
    deleted = False
    user = factory.SubFactory(UserFactory)