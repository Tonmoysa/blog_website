from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='App_Blog'
urlpatterns = [
  path('',views.BlogList.as_view(),name='blog_list'),
  path('write/',views.CreateBlog.as_view(),name='create_blog'), 
  path('blog_details/<slug:slug>/',views.blog_details,name='blog_details'),
  path('liked/<pk>/',views.liked,name='liked_post'),
  path('unliked/<pk>/',views.unliked,name='unliked_post'),
  path('my-blog/',views.MyBlog.as_view(),name='my_blogs'),
  path('update-blog/<int:pk>/', views.UpdateBlog.as_view(), name='edit_blog'),
  path('delete/<int:pk>/', views.DeleteBlog.as_view(), name='delete_blog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 