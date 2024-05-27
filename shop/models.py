from django.db import models
from django.utils.text import slugify
import random
import string

def random_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True, verbose_name='Категория')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,null=True, verbose_name='Родительская категория')
    slug=models.SlugField(max_length=250, unique=True, null=False, editable=True, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k)
            k=k.parent
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(random_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

