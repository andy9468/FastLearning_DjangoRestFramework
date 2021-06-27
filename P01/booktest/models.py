from django.db import models


# Create your models here.
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()
    bread = models.IntegerField(blank=True, null=True)
    bcomment = models.IntegerField(blank=True, null=True, verbose_name='评论量')
    is_delete = models.IntegerField(default=False)

    def __str__(self):
        return self.btitle


class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.IntegerField()
    hcontent = models.CharField(max_length=100)
    hbook = models.ForeignKey("Bookinfo")
    is_delete = models.IntegerField(default=False)

    def __str__(self):
        return self.hname
