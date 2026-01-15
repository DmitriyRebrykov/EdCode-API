from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    LEVELS = [
            ("beginner", "Beginner"),
            ("middle", "Middle"),
            ("advanced", "Advanced"),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)

    level = models.CharField(max_length=50, choices=LEVELS, default="beginner")

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    video_url = models.URLField(blank=True)
    duration = models.PositiveIntegerField(help_text="Длительность в минутах", default=0)

    order = models.PositiveIntegerField(default=1)
    is_free = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title