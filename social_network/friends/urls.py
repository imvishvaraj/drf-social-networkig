from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, PendingFriendRequestsView, UserFriendsListView


urlpatterns = [
    path('<int:user_id>/', UserFriendsListView.as_view(), name='user_friends'),
    path('requests/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('requests/pending/', PendingFriendRequestsView.as_view(), name='pending_friend_requests'),
    path('requests/<uuid:request_id>/accept/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('requests/<uuid:request_id>/reject/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
]
