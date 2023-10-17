from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import (
    Company,
    Recruit,
    Application,
)

from users.models import User


class ApplicationTestCase(TestCase):
    def setUp(self) -> None:

        self.company = Company.objects.create(name="wanted_lab")

        self.recruit = Recruit.objects.create(
            title="wanted-lab backend developer",
            company=self.company,
            skill="pytho, django",
            position="junior",
            description="Welcome to wanted-lab",
        )

        self.user = User.objects.create(username="user_0")

    def test_apply_and_unique_user_recruit(self):

        application = Application.objects.create(user=self.user, recruit=self.recruit)

        self.assertEqual(self.user, application.user)
        self.assertEqual(self.recruit, application.recruit)

        try:

            duplicated_application = Application.objects.create(
                user=self.user, recruit=self.recruit
            )
        except IntegrityError:
            pass
        else:
            self.fail("application model unique constraint is not working.")
