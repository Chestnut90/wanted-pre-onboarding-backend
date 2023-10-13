from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from ..models import Company, Recruit

factory = APIRequestFactory()


class RecruitsAPITestCase(APITestCase):
    """
    Recruits ViewSet api test case.
    """

    client = APIClient(enforce_csrf_checks=True)
    url = "/recruits/"

    def setUp(self) -> None:

        # user login
        user = User.objects.create(username="user")
        self.client.force_login(user)

        # default recruit
        self.company = Company.objects.create(name="company")
        self.recruit = Recruit.objects.create(
            title="title",
            company=self.company,
            skill="skill",
            position="position",
            description="description",
        )

        return super().setUp()

    def test_post_recruit(self):

        # previous recruits
        previous_count = Recruit.objects.count()

        company = Company.objects.create(name="company")
        recruit = {
            "title": "title2",
            "company": company.pk,
            "skill": "skill2",
            "position": "position2",
            "description": "description2",
        }

        response = self.client.post(self.url, data=recruit, format="json")
        self.assertEqual(response.status_code, 201)  # status 201, posted

        current_count = Recruit.objects.count()
        self.assertEqual(current_count, previous_count + 1)  # post 1 recruit

        ret = Recruit.objects.last()
        self.assertEqual(recruit["title"], ret.title)
        self.assertEqual(recruit["company"], ret.company.pk)
        self.assertEqual(recruit["skill"], ret.skill)
        self.assertEqual(recruit["position"], ret.position)
        self.assertEqual(recruit["description"], ret.description)

    def test_get_recruit(self):
        # create company and recruit
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # status 200

        json = response.json()
        self.assertEqual(json["count"], 1)  # count of recruit

    def test_put_recruit(self):

        first = Recruit.objects.first()
        data = {
            "title": "title2",
            "company": 2,
            "skill": "skill2",
            "position": "position2",
            "description": "description2",
        }
        response = self.client.put(self.url + f"{first.pk}/", data=data)
        self.assertEqual(response.status_code, 200)

        updated = Recruit.objects.first()
        self.assertEqual(updated.title, data["title"])
        self.assertNotEqual(updated.company.pk, data["company"])
        self.assertEqual(updated.skill, data["skill"])
        self.assertEqual(updated.position, data["position"])
        self.assertEqual(updated.description, data["description"])

    def test_delete_recruit(self):

        previous_count = Recruit.objects.count()

        first = Recruit.objects.first()
        response = self.client.delete(self.url + f"{first.pk}/")
        self.assertEqual(response.status_code, 204)

        current_count = Recruit.objects.count()
        self.assertEqual(previous_count, current_count + 1)
