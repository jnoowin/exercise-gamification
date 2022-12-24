from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


# Create your models here.
class Workout(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField("Date/Time")
    duration = models.IntegerField("Duration", default=0)
    workout_type = models.CharField(
        "Type of Workout", max_length=50, blank=True)
    calories = models.IntegerField("Calories Burned", default=0)

    def __str__(self):
        return ("user: " + self.user.username + ", date: " + self.date.strftime("%m/%d/%Y, %H:%M:%S")
                + ", duration:" + str(self.duration) + ", workout_type" + self.workout_type + ", calories: " + str(self.calories))


class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    duration = models.IntegerField("Duration", default=0)
    calories = models.IntegerField("Calories", default=0)
    streak = models.IntegerField("Streak", default=0)
    level = models.IntegerField("Level", default=1)
    progress = models.IntegerField("Progress", default=0)
    progressTotal = models.IntegerField("ProgressTotal", default=0)
    max_exp = models.IntegerField("Progress", default=200)
    percentage = models.IntegerField("Progress", default=0)

class QuestCompleted(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed = models.BooleanField("Completed", default=False)
    completion_date = models.DateTimeField("Completion Date", auto_now=True)

    def is_new_day(self):
        return timezone.now() - self.completion_date >= datetime.timedelta(days=1)
