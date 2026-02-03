from django.db import models

# Create your models here.
# models.py -> where database tables for app is defined
# model -> a table in the database
# each attribute -> a column inside the table

# creating new database table called Attendee
class Attendee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()  # no unique=True -> duplicate emails allowed
    registered_at = models.DateTimeField(auto_now_add=True)  # automatically stores timestamp