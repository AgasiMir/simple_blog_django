from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('detail/<slug:post_url>/', views.PostDetailView.as_view(), name='detail'),
    path('tag/<str:tag>/', views.TagView.as_view(), name='tag'),
    path('signup/', views.UserRegistrationView.as_view(), name='signup'),
    path('signin/', views.UserLoginView.as_view(), name='signin'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
