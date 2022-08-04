# from django.db import models
#
#
# # Create your models here.
# class UserProfile(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     first_name = models.CharField(max_length=100)
#     middle_name = models.CharField(max_length=100, blank=True, null=True)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, unique=True)
#     date_of_birth = models.DateField(null=True)
#     bio = models.TextField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.username
