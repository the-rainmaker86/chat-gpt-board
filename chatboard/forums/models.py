from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint, choices 
import string 

import lorem
# from forums.profile import Profile
def seed_users(num):
    for _ in range(num):
        # Loop until a unique username is found.
        while True:
            username = f"user{randint(1, 10000)}"
            if not User.objects.filter(username=username).exists():
                break
        # Use create_user so the password is hashed properly.
        user = User.objects.create_user(username=username, password=f"password{randint(1, 1000000)}")
        print(f"Created user: {user.username}")
        
class Post(models.Model):
                
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Add a self-referential field for threaded comments
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
        
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure the user has a profile; if not, create one.
    Profile.objects.get_or_create(user=instance)
