from .models import UserProfile
from django.contrib.auth.models import User

'''
    Sets the given user's resources (currency) to the given value
'''
def set_resource(resource, username):
    UserProfile.objects
    User.objects

    user = UserProfile(user=User(username=username))

    user.resource = resource
    user.save()

'''
    Get's the given user's resources
'''
def get_resource(username):
    UserProfile.objects
    User.objects

    user = UserProfile(user=User(username=username))

    resource = user.resource
    return resource