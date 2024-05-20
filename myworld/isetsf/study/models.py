from django.db import models
from django.contrib.auth.models import User

class Poste(models.Model):
    CAT_CHOICES = [
        (0, 'Transport'),
        (1, 'Logement'),
        (2, 'Stage'),
        (3, 'Evenement'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now_add=True)  # Set default value to current date
    description=models.TextField(default=" ",max_length=500)
    image = models.ImageField(upload_to='post_images/')
    cat = models.IntegerField(choices=CAT_CHOICES, default=0)

    def __str__(self):
        return f"Date: {self.date} reaction: {self.reactions}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

class Reaction(models.Model):
    post = models.ForeignKey(Poste, on_delete=models.CASCADE, related_name='post_reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reactions')
    comment = models.CharField(max_length=500)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def react_per_post(cls, post_id):
        reactions_per_post = cls.objects.filter(post_id=post_id)
        return reactions_per_post

    

    def __str__(self):
        return f"Reaction to Post {self.post}"


