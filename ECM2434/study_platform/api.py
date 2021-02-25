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


class Poster(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_tag = models.CharField(max_length=64)
    post_pin = models.BooleanField(default=False)

    post_title = models.CharField(max_length=64)
    post_content = models.TextField()
    post_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comt_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    comt_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comt_type = models.CharField(max_length=1)  # C-comment, R-reply, P-post
    comt_pid = models.CharField(max_length=64)
    comt_content = models.TextField()
    comt_time = models.DateTimeField(auto_now=True)
    comt_like = models.IntegerField()
