from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest, UserAccount, Friendship
from .serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer, FriendRequestSerializer


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            context = {
                "id": serializer.data['id'],
                "email": serializer.data['email'],
                "message": "Account Created."
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            serializer = UserLoginSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserDetailSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(ListAPIView):
    serializer_class = UserDetailSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = UserAccount.objects.all()
        email = self.request.query_params.get('email', None)
        name = self.request.query_params.get('name', None)

        if email is not None:
            queryset = queryset.filter(email=email)
        elif name is not None:
            queryset = queryset.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        return queryset


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(from_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(APIView):
    def post(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        if friend_request.to_user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        friend_request.accept()
        return Response(status=status.HTTP_200_OK)


class RejectFriendRequestView(APIView):
    def post(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        if friend_request.to_user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        friend_request.reject()
        return Response(status=status.HTTP_200_OK)


class PendingFriendRequestsView(ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')


class UserFriendsListView(ListAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        friendships = Friendship.objects.filter(Q(user1_id=user_id) | Q(user2_id=user_id))
        friend_ids = [friendship.user2_id if friendship.user1_id == user_id else friendship.user1_id for friendship in friendships]
        return UserAccount.objects.filter(id__in=friend_ids)
