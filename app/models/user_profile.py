from app.models import Model
from django.db import models
from django.contrib.auth.models import User

class UserProfile(Model):
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
      return self.user.__unicode__() + "'s Profile"

# Create an easy way to use the user profile
# using user.profile will get or create a user profile
# object
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])