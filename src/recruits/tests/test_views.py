from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from ..models import Company, Recruit

from users.models import User

factory = APIRequestFactory()


class RecruitsAPITestCase(APITestCase):
    """
    Recruits ViewSet api test case.
    """

    client = APIClient(enforce_csrf_checks=True)
    url = "/recruits/"

    def setUp(self) -> None:
        self.default_manager = User.objects.create(
            username="default_user", is_manager=True
        )
        self.default_company = Company.objects.create(
            name="company", manager=self.default_manager
        )
        self.default_recruit = Recruit.objects.create(
            title="title",
            company=self.default_company,
            skill="skill",
            position="position",
            description="description",
        )
        return super().setUp()

    def test_post_recruit(self):

        # previous recruits
        previous_count = Recruit.objects.count()

        recruit = {
            "title": "title2",
            "skill": "skill2",
            "position": "position2",
            "description": "description2",
        }

        # anonymous user cannot post recruit
        self.client.logout()
        response = self.client.post(self.url, data=recruit, format="json")
        self.assertEqual(response.status_code, 403)  # forbidden

        # normal user can not post recruit
        user = User.objects.create(username="user", is_manager=False)
        self.client.force_login(user)
        response = self.client.post(self.url, data=recruit, format="json")
        self.assertEqual(response.status_code, 403)  # permission denied, forbidden

        # manager user can post recruit
        self.client.force_login(self.default_manager)
        response = self.client.post(self.url, data=recruit, format="json")
        self.assertEqual(response.status_code, 201)  # status 201, posted
        self.assertEqual(Recruit.objects.count(), previous_count + 1)  # post 1 recruit

        json = response.json()
        self.assertEqual(recruit["title"], json["title"])
        self.assertEqual(recruit["skill"], json["skill"])
        self.assertEqual(recruit["position"], json["position"])
        self.assertEqual(recruit["description"], json["description"])
        self.assertEqual(self.default_company.pk, json["company"])

    def test_get_recruit(self):
        # get method allowed to all

        self.client.logout()  # unauth
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # status 200

        json = response.json()
        self.assertEqual(json["count"], Recruit.objects.count())  # count of recruit

        # TODO : search test.

    def test_update_recruit(self):
        """recruits update method"""

        url = f"{self.url}{self.default_recruit.pk}/"
        data = {
            "title": "changed",
            "company": "changed",
            "position": "changed",
            "skill": "changed",
            "description": "changed",
        }

        # anonymous user cannot update recruit
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 403)  # forbidden

        # normal user cannot update recruit
        user = User.objects.create(username="user")
        self.client.force_login(user)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 403)  # forbidden

        # other manager user cannot delete recruit
        other_manager = User.objects.create(username="other_manager", is_manager=True)
        self.client.force_login(other_manager)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 403)  # forbidden

        # recruit owner(manager) can delete recruit
        self.assertEqual(self.default_manager, self.default_recruit.company.manager)
        self.client.force_login(self.default_manager)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)  # updated

        updated = Recruit.objects.first()
        self.assertEqual(updated.title, data["title"])
        self.assertEqual(updated.skill, data["skill"])
        self.assertEqual(updated.position, data["position"])
        self.assertEqual(updated.description, data["description"])

    def test_delete_recruit(self):
        """recruits delete method"""
        previous_count = Recruit.objects.count()

        url = f"{self.url}{self.default_recruit.pk}/"

        # anonymous user cannot delete recruit
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)  # forbidden
        self.assertEqual(previous_count, Recruit.objects.count())

        # normal user cannot delete recruit
        user = User.objects.create(username="user")
        self.client.force_login(user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)  # forbidden
        self.assertEqual(previous_count, Recruit.objects.count())

        # other manager user cannot delete recruit
        other_manager = User.objects.create(username="other_manager", is_manager=True)
        self.client.force_login(other_manager)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)  # forbidden
        self.assertEqual(previous_count, Recruit.objects.count())

        # recruit owner(manager) can delete recruit
        self.assertEqual(self.default_manager, self.default_recruit.company.manager)
        self.client.force_login(self.default_manager)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)  # no content
        self.assertEqual(previous_count - 1, Recruit.objects.count())

    def test_application(self):

        url = f"{self.url}{self.default_recruit.pk}/application/"

        # anonymous user cannot apply to recruit
        self.client.logout()
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 403)  # forbidden

        # manager user cannot apply to recruit
        self.client.force_login(self.default_manager)
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 403)  # forbidden

        # other manager cannot apply to recruit
        other_manager = User.objects.create(username="other_manager", is_manager=True)
        self.client.force_login(other_manager)
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 403)  # forbidden

        # user can apply to recruit
        user = User.objects.create(username="user")
        self.client.force_login(user)
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 201)  # created
