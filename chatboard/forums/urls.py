from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/reply/', views.add_reply, name='add_reply'),
    path('me/<str:username>/', views.profile, name='profile'),
    path('profile/customize/', views.customize_profile, name='customize_profile'),
]
