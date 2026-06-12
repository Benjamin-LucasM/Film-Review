from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings

def get_fernet():
    return Fernet(settings.FERNET_KEY.encode())

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    director = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True) 

    def __str__(self):
        return f"{self.title} ({self.year})"

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        f = get_fernet()
        token = f.encrypt(self.text.encode())
        self.text = token.decode()
        super().save(*args, **kwargs)

    def get_decrypted_text(self):
        f = get_fernet()
        token = self.text.encode()
        return f.decrypt(token).decode()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"