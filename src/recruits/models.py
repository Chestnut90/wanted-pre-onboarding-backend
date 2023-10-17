from django.db import models

# Create your models here.


class TimeTrackingModelBase(models.Model):
    """
    Time model base class of created_at, updated_at fields
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Company(TimeTrackingModelBase):
    """
    Company model class.
    """

    name = models.TextField(max_length=100)

    # TODO : not null ?
    manager = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, null=True, related_name="company"
    )

    def __str__(self) -> str:
        return self.name


class Recruit(TimeTrackingModelBase):
    """
    Recruit model class.
    """

    title = models.TextField(max_length=100)
    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        null=False,
        related_name="recruits",
    )

    skill = models.TextField(max_length=100)
    position = models.TextField(max_length=100)

    # details on below

    description = models.TextField(max_length=500)


class Application(TimeTrackingModelBase):
    """
    Application model class. record relationship user with recruit.
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recruit"], name="unique_user_to_recruit"
            ),
        ]

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="users",
    )
    recruit = models.ForeignKey(
        "Recruit",
        on_delete=models.CASCADE,
        related_name="recruits",
    )
