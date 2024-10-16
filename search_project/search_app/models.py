from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table="category"



    
class Product(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    # 1 はカテゴリ ID
    def __str__(self):
        return self.name
    
    class Meta:
        db_table="product"