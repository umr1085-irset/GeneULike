from typing import Any, Sequence

from factory import DjangoModelFactory, Faker, post_generation
from geneulike.groups.models import Group

class GroupFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = Group
