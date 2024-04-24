from django.urls import path
from .views import UserRegisterView, UserLoginView, UserDetailView
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, PendingFriendRequestsView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('friend-request/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending_friend_requests'),
    path('friend-request/<uuid:request_id>/accept/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friend-request/<uuid:request_id>/reject/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
]
