from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from django.utils.translation import ugettext_lazy as _
import uuid


class Application(models.Model):
    pass


class Record(models.Model):
    pass


class Society(models.Model):
    pass


class Team(models.Model):
    pass


class Course(models.Model):
    code = models.CharField(max_length=7, primary_key=True)
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.code + " " + self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64)
    dob = models.DateField()
    gold = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    course = models.ManyToManyField(Course, blank=True, null=True)
    team = models.ManyToManyField(Team, blank=True, null=True)
    society = models.ManyToManyField(Society, blank=True, null=True, through="Society_Membership")
    avatar = models.ImageField(upload_to="/avatar"+str(User.username))


class Society_Membership(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_join = models.DateField(auto_now_add=True)
    level = models.IntegerField(default=0)


class Tag(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Card(models.Model):
    card_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_type = models.IntegerField()
    card_tags = TaggableManager(blank=True, through=Tag)
    card_content = models.TextField()
    card_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    card_create_date = models.DateTimeField(auto_now_add=True)

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
    coll_tags = TaggableManager(blank=True, through=Tag)
    coll_description = models.CharField(max_length=512)
    coll_cards = models.ManyToManyField(Card)
    coll_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    coll_create_date = models.DateTimeField(auto_now_add=True)


class Blog(models.Model):
    blog_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    blog_user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_tags = TaggableManager(blank=True, through=Tag)
    blog_pin = models.BooleanField(default=False)

    blog_title = models.CharField(max_length=64)
    blog_content = models.TextField()
    blog_time = models.DateTimeField(auto_now=True)

    def get_tags(self):
        self.blog_tags.names()


class Comment(models.Model):
    comt_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    comt_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comt_type = models.CharField(max_length=1)  # C-comment, R-reply, P-post
    comt_father_id = models.CharField(max_length=64)
    comt_content = models.TextField()
    comt_time = models.DateTimeField(auto_now=True)
    comt_like = models.IntegerField()

