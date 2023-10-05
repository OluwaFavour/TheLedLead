from django.urls import path
from .views import (
    ListBooksView,
    bookView,
    addCommentsView,
    commentView,
    replyToCommentView,
    editCommentView,
    deleteCommentView,
    addRatingView,
    likeCommentView,
    getCommentLikesView,
)

urlpatterns = [
    path("", ListBooksView.as_view(), name="book_list"),
    path("<int:id>/", bookView, name="book_detail"),
    path("comment/add/<int:book_id>/", addCommentsView, name="add_comment"),
    path("comment/<int:comment_id>/", commentView, name="comment_detail"),
    path("comment/reply/<int:comment_id>/", replyToCommentView, name="reply_comment"),
    path("comment/edit/<int:comment_id>/", editCommentView, name="edit_comment"),
    path("comment/delete/<int:comment_id>/", deleteCommentView, name="delete_comment"),
    path("comment/like/<int:comment_id>/", likeCommentView, name="like_comment"),
    path("comment/likes/<int:comment_id>/", getCommentLikesView, name="get_comment_likes"),
    path("rate/<int:id>/", addRatingView, name="add_rating"),
]
