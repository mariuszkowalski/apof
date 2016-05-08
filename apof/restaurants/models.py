from django.db import models


class Restaurant(models.Model):
	name = models.CharField(max_length=256)
	phone = models.CharField(max_length=64)
	open_at_mon = models.CharField(max_length=32)
	close_at_mon = models.CharField(max_length=32)
	open_at_tue = models.CharField(max_length=32)
	close_at_tue = models.CharField(max_length=32)
	open_at_wed = models.CharField(max_length=32)
	close_at_wed = models.CharField(max_length=32)
	open_at_thu = models.CharField(max_length=32)
	close_at_thu = models.CharField(max_length=32)
	open_at_fri = models.CharField(max_length=32)
	close_at_fri = models.CharField(max_length=32)
	open_at_sat = models.CharField(max_length=32)
	close_at_sat = models.CharField(max_length=32)
	open_at_sun = models.CharField(max_length=32)
	close_at_sun = models.CharField(max_length=32)

	
	def  __repr__(self):
		return 'name="{}", phone="{}"'.format(self.name, self.phone)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class Ingredients(models.Model):
	ingredient_name = models.CharField(max_length=256)

	def __repr__(self):
		return 'ingredient name="{}"'.format(self.ingredient_name)

	class Meta:
		ordering = ('ingredient_name',)

	def __str__(self):
		return self.ingredient_name


class Meal(models.Model):
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	ingredients = models.ManyToManyField(Ingredients)
	meal_name = models.CharField(max_length=256)
	spicy = models.CharField(max_length=32)
	price_s = models.CharField(max_length=32)
	price_m = models.CharField(max_length=32)
	price_l = models.CharField(max_length=32)

	def __repr__(self):
		return 'meal name="{}", spicy="{}" ,price s="{}", price m="{}", price l="{}"'.\
			format(self.meal_name, self.spicy, self.price_s, self.price_m, self.price_l)

	class Meta:
		ordering = ('meal_name',)

	def __self__(self):
		return self.meal_name