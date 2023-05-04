from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class News(models.Model):
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    image = models.ImageField(null=True, upload_to='news')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 null=True, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тэги')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    link = models.URLField(verbose_name='Ссылка')
    text = models.TextField(null=True, verbose_name='Текст')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    rating = models.FloatField(default=0, verbose_name='Рейтинг')
    date_off = models.DateField(null=True, verbose_name='Дата окончания новости')

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        ordering = ['-created_at']
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateField(null=True,
                                  auto_now_add=True)

    def __str__(self):
        return self.text
