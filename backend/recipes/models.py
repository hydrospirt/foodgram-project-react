from django.db import models


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        )
    text = models.TextField(
        verbose_name='Описание',
        max_length=5000,
        )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=1,
        )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )



    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})