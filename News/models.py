from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  
    content = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,   
        related_name='news'
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)      
    published_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    

class ImageModel(models.Model):
    news=models.ForeignKey(News,on_delete=models.CASCADE,related_name='image')
    image = models.ImageField(upload_to="news_images/", blank=True, null=True)




class Comment(models.Model):
    news=models.ForeignKey(News,on_delete=models.CASCADE,related_name='comment')
    user=models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE,related_name='user')
    content=models.TextField()
    is_approved = models.BooleanField(default=True)
    def __str__(self):
        
        return f"Comment by {self.user} on {self.news}"

class Advertisement(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="ads_images/", blank=True, null=True)
    is_active = models.BooleanField(default=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]  
