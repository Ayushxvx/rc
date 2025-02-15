from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Usertype(models.Model):
    USER_TYPE_CHOICES = [
        ('host','Host'),
        ('attendee','Attendee')
    ]
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    document_proof = models.ImageField(upload_to="document_proofs/")
    phone_no = models.IntegerField(null=True)

class Post(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.TextField()
    Ticket_fare = models.IntegerField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField(default=timezone.now())
    status = models.TextField(default="upcoming")

class Like(models.Model):
    post = models.ForeignKey(Post,related_name="likes",on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name="likes",on_delete=models.CASCADE)

class Dislike(models.Model):
    post = models.ForeignKey(Post,related_name="dislikes",on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name="dislikes",on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    platform_fees = 5
    event = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="ticket")
    buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

class Subscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fees = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()