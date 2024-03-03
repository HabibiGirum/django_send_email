from django.urls import path
from . import views


urlpatterns = [
    path('index/<str:mac_address>/', views.index, name='index'),
    # path('projects/', views.projects, name='projects'),
    # path('projects/<int:id>', views.singleProject, name='single-project'),

    # path('messages/', views.inbox, name='inbox'),
    # path('messages/<int:id>', views.singleMessage, name='message'),
    path('login/', views.sendMessage, name='sendMessage'),
]
