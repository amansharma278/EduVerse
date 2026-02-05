from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    password = models.CharField(max_length=15)
    account_type = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    about = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "user"

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_description = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    what_you_will_learn = models.CharField(max_length=500)
    price = models.FloatField()
    thumbnail = models.CharField(max_length=500)
    class Meta:
        db_table = "course"

class Section(models.Model):
    id = models.AutoField(primary_key=True)
    sec_name =models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)

    class Meta:
        db_table = "section"

class SubSection(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    time_durastation = models.DateTimeField(max_length=100)
    description = models.CharField(max_length=100)
    video_url = models.CharField(max_length=500)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    class Meta:
        db_table = "sub_section"


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    class Meta:
        db_table = "tag"

class CourseTag(models.Model):
    id = models.AutoField(primary_key=True)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        db_table = "course_tag"


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_progress = models.FloatField(default=0.0)
    price  = models.IntegerField(default=0)
    class Meta:
        db_table = "invoice"

class UserCourse(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_progress = models.FloatField(default=0.0)

    class Meta:
        db_table = "user_course"


class RatingReview(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = "rating_review"

class Token(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    issue_at = models.DateTimeField()
    expired_at = models.DateTimeField()
