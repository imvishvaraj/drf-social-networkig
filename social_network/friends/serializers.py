from rest_framework import serializers
from users_app.models import UserAccount
from users_app.serializers import UserDetailSerializer
from friends.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserDetailSerializer(read_only=True)
    to_user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'status']

    def create(self, validated_data):
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)


class PendingFriendRequestSerializer(FriendRequestSerializer):
    from_user = UserDetailSerializer()

    class Meta(FriendRequestSerializer.Meta):
        fields = FriendRequestSerializer.Meta.fields + ['from_user']
