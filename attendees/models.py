from django.db import models

# Create your models here.
# models.py -> where database tables for app is defined
# model -> a table in the database
# each attribute -> a column inside the table

class Attendee(models.Model):                                   # creating new database table called Attendee
    name = models.CharField(max_length=100)                     # text field for name
    email = models.EmailField(unique=True)                      # email field, unique=True means 2 people cannot register with same email
    registered_at = models.DateTimeField(auto_now_add=True)     # automatically stores time registered

    def __str__(self):      # makes admin panel show name instead of "Attendee object"
        return self.name
