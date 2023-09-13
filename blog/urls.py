from django.urls import include, path
import blog.views as views

urlpatterns = [
    path("", views.listBooks, name="listBooks_view"),
]