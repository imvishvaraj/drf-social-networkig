import uuid
from django.db import models
from users_app.models import UserAccount


class Friendship(models.Model):
    user1 = models.ForeignKey(UserAccount, related_name='friendships_initiated', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserAccount, related_name='friendships_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(UserAccount, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserAccount, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def accept(self):
        Friendship.objects.create(user1=self.from_user, user2=self.to_user)
        self.status = 'accepted'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()
