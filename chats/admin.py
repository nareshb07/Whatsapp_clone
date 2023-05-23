from django.contrib import admin
from chats.models import ChatModel  , ChatNotification #, UserProfileModel
# Register your models here.
admin.site.register(ChatModel)
#admin.site.register(UserProfileModel)
admin.site.register(ChatNotification)


from .models import Follower, Creator, User



admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Creator)

