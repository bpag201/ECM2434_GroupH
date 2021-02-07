from django.db import models
from django.utils.translation import gettext_lazy as _

""" One thing I'm not sure: I don't know if it's appropriate to use auto_now / auto_now_add options in the 
    DateTimeFields, if someone could check if I used these options correctly it will be great. Thanks."""

""" About creating tables to handle many-to-one relationship: By using django we don't need to do this anymore, as 
    django has a function to return all related models to a model."""

""" Still trying to figure out how image fields work """


class Course(models.Model):
    name = models.CharField(max_length=20)


class User(models.Model):
    class Tiers(models.TextChoices):
        STUDENT = "STU", _("Student")
        STAFF = "STF", _("Staff")
        ADMIN = "ADM", _("Admin")
        WELFARE = "WEL", _("Welfare")

    password = models.CharField()
    full_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=320)
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

    # inventory: I plan to implement inventory by calling the user.reward_set.all() function which returns all related
    # loots

    def __str__(self):
        return self.full_name


class Team(models.Model):
    name = models.CharField(max_length=20)
    manager = models.ForeignKey(User, on_delete=models.PROTECT)

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
    title = models.CharField()
    category = models.CharField(max_length=3, choices=Categories, default=Categories.STUDYNOTE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL)  # If we allow multiple participants then don't use this
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField()

    def __str__(self):
        return self.title


""" Blog specified for teams """


class TeamBlog(models.Model):
    title = models.CharField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL)  # If we allow multiple participants then don't use this
    team = models.ForeignKey(Team, on_delete=models.SET_NULL)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)


""" Each comment belongs to one blog and has one author """


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now=True)


class Quiz(models.Model):
    is_welfare = models.BooleanField()
    id = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


""" Each Question has a related course, and is bind to a quiz """


class Question(models.Model):
    class Categories(models.TextChoices):
        MULTIPLE_CHOICE = "MUL", _("Multiple Choice")
        FILL_BLANK = "FIB", _("Fill Blank")

    category = models.CharField(max_length=3, choices=Categories)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL)
    content = models.TextField()
    answer = models.TextField()


""" Only store results of welfare quizzes, this needs to be done in backend code by checking is_welfare attribute
    of a quiz model"""


class WelfareResult(models.Model):
    date = models.DateTimeField(auto_now=True)
    percentage = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL)


""" This only contains achievements users have, not all possibilities """


class Achievement(models.Model):
    name = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


""" Loots """


class Reward(models.Model):
    class Effect(models.TextChoices):
        EMPTY = "EMP", _("Empty")

    name = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_tool = models.BooleanField()
    description = models.TextField()
    # has_mods -> I don't think we need this as we only need to bind mods to a reward
    effect = models.CharField(max_length=3, choices=Effect, default=Effect.EMPTY)
    graphic = models.ImageField()

    def __str__(self):
        return self.name


class Accessory(models.Model):
    name = models.CharField()
    description = models.TextField()
    graphic = models.ImageField()
    target = models.ForeignKey(Reward, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mod(models.Model):
    name = models.CharField()
    description = models.TextField()
    effect = models.CharField()  # Assuming effects can be applied by changing some parameters. 
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class UserTitle(models.Model):
    content = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


""" User might be assigned to a team, this creates a column to store the corresponding information """
User.team = models.ForeignKey(Team, on_delete=models.SET_NULL)
""" Create column to let courses bind with colleges """
Course.college = models.ForeignKey(College, on_delete=models.CASCADE)
