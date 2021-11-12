from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):

    """Conversation Model Definition"""

    participants = models.ManyToManyField("users.User", blank=True)
    # participants = models.ManyToManyField(
    #     "users.User", related_name="converstation", blank=True
    # )

    # def __str__(self):
    #     return str(self.create)
    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        # print(self.message_set.all())
        # # <QuerySet [<message: <yamizora>seys : awegraehaehreah>]> /
        # <QuerySet [<message: <yamizora>seys : 메세지 안에 메세지1>,
        # <message: <hosibito>seys : apapapap02>]>
        # print(self.message_set.all().count())  # 1  / 2
        # print(self.message_set.all()[0].message)  # awegraehaehreah  /  메세지 안에 메세지1
        return self.message_set.count()

    count_messages.short_description = "메세지 갯수"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "맴버 수"


class Message(core_models.TimeStampedModel):

    """Message Model Definition"""

    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    # user = models.ForeignKey(
    #     "users.User", related_name="messages", on_delete=models.CASCADE
    # )
    # conversation = models.ForeignKey(
    #     "Conversation", related_name="messages", on_delete=models.CASCADE
    # )

    def __str__(self):
        return f"{self.user} says: {self.message}"
