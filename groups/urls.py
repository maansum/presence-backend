from django.urls import path
from groups.views import GroupCreateView,UpdateGroupNameView,GetAllGroupCreatedView,DeleteGroupView, AttendeesView,AttendeesOfGroup,InvolvedGroupView,RecommendedView


urlpatterns=[
    path('create/',GroupCreateView.as_view(),name='create_group'),
    path('update/<int:pk>/',UpdateGroupNameView.as_view(),name='update name'),
    path('groups/',GetAllGroupCreatedView.as_view(),name='getall group'),
    path('delete/<int:pk>',DeleteGroupView.as_view(),name='delete group'),
    path('attendees/' ,AttendeesView.as_view(), name='attendees'),
    path('attendeesOfGroup/<int:pk>/' ,AttendeesOfGroup.as_view(), name='attendees'),
    path('involvement/',InvolvedGroupView.as_view(), name='involvement'),
    path('recomendation/',RecommendedView.as_view(), name='group recomend'),
    
]
