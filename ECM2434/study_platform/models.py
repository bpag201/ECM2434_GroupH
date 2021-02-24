from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

""" One thing I'm not sure: I don't know if it's appropriate to use auto_now / auto_now_add options in the 
    DateTimeFields, if someone could check if I used these options correctly it will be great. Thanks."""

""" About creating tables to handle many-to-one relationship: By using django we don't need to do this anymore, as 
    django has a function to return all related models to a model."""

""" Still trying to figure out how image fields work """


class Course(models.Model):
    name = models.CharField(max_length=20)


class UserProfile(models.Model):
    class Tiers(models.TextChoices):
        STUDENT = "STU", _("Student")
        STAFF = "STF", _("Staff")
        ADMIN = "ADM", _("Admin")
        WELFARE = "WEL", _("Welfare")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    score = models.IntegerField()
    resource = models.IntegerField()
    avatar = models.ImageField()
    user_tier = models.CharField(
        max_length=3,
        choices=Tiers.choices,
        default=Tiers.STUDENT
    )
    REQUIRED_FIELD = ['full_name', 'email', 'nickname', 'course', 'user_tier']

   
    # inventory: I plan to implement inventory by calling the user.reward_set.all() function which returns all related
    # loots

    def __str__(self):
        return self.full_name


class Team(models.Model):
    name = models.CharField(max_length=20)
    manager = models.ForeignKey(UserProfile, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class College(models.Model):
    name = models.CharField(max_length=20)
    score = models.IntegerField()

    def __str__(self):
        return self.name


""" The blog includes different categories 
    And belongs to one college / has one author"""


class Blog(models.Model):
    class Categories(models.TextChoices):
        STUDYNOTE = "STN", _("Study Note")

    post_to = models.ForeignKey(College, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    category = models.CharField(max_length=3, choices=Categories.choices, default=Categories.STUDYNOTE)
    content = models.TextField()
    #author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="author")  # If we allow multiple participants then don't use this
    participants = models.ManyToManyField(UserProfile)                       # Well ...
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField()

    def __str__(self):
        return self.title


""" Blog specified for teams """


class TeamBlog(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    #author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # If we allow multiple participants then don't use this
    participants = models.ManyToManyField(UserProfile)                  # Well ...
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)


""" Each comment belongs to one blog and has one author """


class Comment(models.Model):
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now=True)


class Quiz(models.Model):
    is_welfare = models.BooleanField()
    id = models.CharField(max_length=50, primary_key=True)
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


""" Each Question has a related course, and is bind to a quiz """


class Question(models.Model):
    class Categories(models.TextChoices):
        MULTIPLE_CHOICE = "MUL", _("Multiple Choice")
        FILL_BLANK = "FIB", _("Fill Blank")

    category = models.CharField(max_length=3, choices=Categories.choices)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    answer = models.TextField()


""" Only store results of welfare quizzes, this needs to be done in backend code by checking is_welfare attribute
    of a quiz model"""


class WelfareResult(models.Model):
    date = models.DateTimeField(auto_now=True)
    percentage = models.IntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, null=True, on_delete=models.SET_NULL)


""" This only contains achievements users have, not all possibilities """


class Achievement(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


""" Loots """


class Reward(models.Model):
    class Effect(models.TextChoices):
        EMPTY = "EMP", _("Empty")
        POLICE = "POL", _("Police")
        THIEF = "THF", _("Thief")
        SHIELD = "SHD", _("Shield")
        BLIND = "BLN", _("Blind")
        BOOST = "BST", _("Boost")

    name = models.CharField(max_length=20)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_tool = models.BooleanField()
    description = models.TextField()
    # has_mods -> I don't think we need this as we only need to bind mods to a reward
    effect = models.CharField(max_length=3, choices=Effect.choices, default=Effect.EMPTY)
    graphic = models.ImageField()

    def __str__(self):
        return self.name


class Accessory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    graphic = models.ImageField()
    has_mods = models.BooleanField()
    target = models.ForeignKey(Reward, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mod(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    effect = models.CharField(max_length=20)  # Assuming effects can be applied by changing some parameters. 
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class UserTitle(models.Model):
    content = models.CharField(max_length=20)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
    
class QuizTag():
    content = models.CharField(max_length=20)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)


""" User might be assigned to a team, this creates a column to store the corresponding information """
UserProfile.team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
""" Create column to let courses bind with colleges """
Course.college = models.ForeignKey(College, on_delete=models.CASCADE)

# Shouldn't reference User directly so we use this instead
# User = get_user_model()

class Card(models.Model):
    card_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_type = models.IntegerField()
    card_content = models.TextField()
    card_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    card_creat_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_content


class Option(models.Model):
    opt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    opt_cid = models.ForeignKey(Card, on_delete=models.CASCADE)
    opt_type = models.CharField(max_length=3, default='TXT')  # IMG - image; TXT - text
    opt_content = models.CharField(max_length=512)
    opt_isCorrect = models.BooleanField(default=False)

    def __str__(self):
        return self.opt_content


class Collection(models.Model):
    coll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coll_title = models.CharField(max_length=64)
    coll_description = models.CharField(max_length=512)
    coll_cards = models.ManyToManyField(Card)
    coll_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    coll_creat_date = models.DateTimeField(auto_now_add=True)


# to be completed
class Poster(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_tag = models.CharField(max_length=64)
    post_pin = models.BooleanField(default=False)

    post_title = models.CharField(max_length=64)
    post_content = models.TextField()
    post_time = models.DateTimeField(auto_now=True)


# to be completed
class Comment(models.Model):
    comt_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    comt_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comt_type = models.CharField(max_length=1)  # C-comment, R-reply, P-post
    comt_pid = models.CharField(max_length=64)
    comt_content = models.TextField()
    comt_time = models.DateTimeField(auto_now=True)
    comt_like = models.IntegerField()
