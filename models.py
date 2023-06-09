from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.db import models


# Create your models here.

class Class(models.Model):
    grade = models.IntegerField()
    division = models.CharField(max_length=1)

    def __str__(self):
        return str(self.grade) + ":" + self.division


class Teacher(models.Model):
    user = models.OneToOneField(User)
    which_class = models.ForeignKey(Class, null=True, default=None)
    name = models.CharField(max_length=100)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Teacher'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return str(self.name) + "-" + str(self.which_class)


class Admin(models.Model):
    user = models.OneToOneField(User)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Admin'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return str(self.name)


class Principal(models.Model):
    user = models.OneToOneField(User)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Principal'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    user = models.OneToOneField(User)
    which_class = models.ForeignKey(Class)
    phone = models.BigIntegerField()
    roll_no = models.IntegerField(unique=False)
    name = models.CharField(max_length=100)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Student'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return self.name


class Parent(models.Model):
    student = models.ForeignKey(User)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    name = models.CharField(max_length=100)


class Attendance(models.Model):
    date = models.DateTimeField()
    student = models.ForeignKey(Student)
    is_present = models.BooleanField(default=True)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    which_class = models.ForeignKey(Class)


class Test(models.Model):
    subject = models.ForeignKey(Subject)
    total_marks = models.IntegerField()
    name = models.CharField(max_length=100, unique=False)
    date = models.DateField()


class Marks(models.Model):
    marks = models.DecimalField(decimal_places=2, max_digits=7)
    test = models.ForeignKey(Test)
    student = models.ForeignKey(Student)


# Experimental feature to be added
'''
class Remarks(models.Model):
    student = models.ForeignKey(User)
    teacher = models.ForeignKey(User)
    remark = models.TextField()
    date = models.DateField()
'''
