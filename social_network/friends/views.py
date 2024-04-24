from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from friends.models import FriendRequest, Friendship
from friends.serializers import FriendRequestSerializer
from users_app.serializers import UserDetailSerializer
from users_app.models import UserAccount


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(from_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        if friend_request.to_user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        friend_request.accept()
        return Response(status=status.HTTP_200_OK)


class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        if friend_request.to_user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        friend_request.reject()
        return Response(status=status.HTTP_200_OK)


class PendingFriendRequestsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')


class UserFriendsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        friendships = Friendship.objects.filter(Q(user1_id=user_id) | Q(user2_id=user_id))
        friend_ids = [friendship.user2_id if friendship.user1_id == user_id else friendship.user1_id for friendship in friendships]
        return UserAccount.objects.filter(id__in=friend_ids)
