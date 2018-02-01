from django.db import models


class DemoModel1(models.Model):
    name = models.CharField(max_length=255)


class DemoModel2(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "DemoModel2 #%s" % self.pk

    def __str__(self):
        return "DemoModel2 #%s" % self.pk


class DemoModel3(models.Model):
    name = models.CharField(max_length=255)


class DemoModel4(models.Model):
    name = models.CharField(max_length=255)
