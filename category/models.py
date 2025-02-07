from django.db import models



class Category(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    parent_category=models.ForeignKey("self",related_name="subcategories",null=True,blank=True,on_delete=models.SET_NULL)
  

    def __str__(self):
        return self.name