from django.contrib import admin
from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """Message Admin Definition"""

    list_display = ("conversation", "__str__", "create")


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """Conversation Admin Definition"""

    pass
