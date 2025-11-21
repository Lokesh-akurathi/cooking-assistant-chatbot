from django.urls import path
from . import views

urlpatterns = [
    path("state/", views.conversation_state, name="conversation_state"),
    path("message/", views.post_message, name="post_message"), 
]
