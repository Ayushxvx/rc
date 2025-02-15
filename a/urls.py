from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("signup",views.signup,name="signup"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("addpost",views.addpost,name="addpost"),
    path("posts",views.posts,name="posts"),
    path("elaborate/<str:id>",views.elaborate,name="elaborate"),
    path("like/<str:id>",views.like,name="like"),
    path("dislike/<str:id>",views.dislike,name="dislike"),
    path("add_comment/<str:id>",views.add_comment,name="add_comment"),
    path("del_comment/<str:id>",views.del_comment,name="del_comment"),
    path("book_ticket/<str:id>/<str:price>",views.book_ticket,name="book_ticket"),
    path("profile",views.profile,name="profile"),
    path("download_ticket/<str:ticket_id>",views.generate_ticket,name="download_ticket"),
    path("subscribe",views.subscribe,name="subscribe"),
    path('sub',views.sub,name="sub")
]