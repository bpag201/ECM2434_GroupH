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
    code = models.CharField(max_length=4, primary_key=True)
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.code + " " + self.title


class Item(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=50)
    item_dscp = models.CharField(max_length=512)
    item_rare = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gold = models.IntegerField(default=0, blank=True, null=True)
    score = models.IntegerField(default=0, blank=True, null=True)
    course = models.ManyToManyField(Course)
    team = models.ManyToManyField(Team)
    society = models.ManyToManyField(Society, through="Society_Membership")
    resources = models.ManyToManyField(Item, through="User_item")
    # avatar = models.ImageField(upload_to="/avatar"+str(User.username))

    def gold_modify(self, amount):
        self.gold += amount


class User_item(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)


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

