from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


def book_image_path(instance, filename):
    # Build the file path based on the book's title
    return f"book_covers/{instance.title}/{filename}"


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    image_url = models.ImageField(upload_to=book_image_path, blank=True, null=True)
    image_url_link = models.URLField(blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    date_published = models.DateTimeField(auto_now=True)
    read_by = models.ManyToManyField(
        User, through="ReadBook", related_name="books_read", blank=True
    )
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date_published"]
        verbose_name = "book"
        verbose_name_plural = "books"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"id": self.id})


class ReadBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_date = models.DateTimeField()

    class Meta:
        unique_together = ("user", "book")


class Comment(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)

    class Meta:
        ordering = ["date_posted"]
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.title}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(5, message="Rating must be at most 5."),
        ]
    )

    class Meta:
        verbose_name = "rating"
        verbose_name_plural = "ratings"

    def __str__(self):
        return f"{self.rating} stars on {self.book.title} by {self.user.username}"
