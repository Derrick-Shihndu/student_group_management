from django.db import models
from django.utils import timezone

class MainGroup(models.Model):
    name = models.CharField(max_length=200)
    join_password = models.CharField(max_length=128)
    notes_password = models.CharField(max_length=128)
    max_members = models.PositiveIntegerField(default=10)
    delegate_phone = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Course(models.Model):
    main_group = models.ForeignKey(MainGroup, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.main_group.name})"

class SubGroup(models.Model):
    main_group = models.ForeignKey(MainGroup, on_delete=models.CASCADE, related_name='subgroups')
    name = models.CharField(max_length=100)
    leader = models.ForeignKey('Student', null=True, blank=True, on_delete=models.SET_NULL, related_name='leading_group')

    def __str__(self):
        return f"{self.name} — {self.main_group.name}"

class Student(models.Model):
    subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE, related_name='members')
    name1 = models.CharField(max_length=200)
    name2 = models.CharField(max_length=200)
    name3 = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40, unique=True)
    courses = models.ManyToManyField(Course, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name1} {self.name2} ({self.phone})"

class GroupNote(models.Model):
    subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Note: {self.title} — {self.subgroup}"

class GroupMessage(models.Model):
    subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Msg @{self.posted_at}: {self.subgroup}"
