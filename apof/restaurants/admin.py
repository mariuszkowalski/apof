from django.contrib import admin
from restaurants.models import Restaurant, Meal, Ingredients

class RestaurantAdmin(admin.ModelAdmin):
	model = Restaurant
	list_display = ['name',
					'phone',
					'open_at_mon',
					'close_at_mon',
					'open_at_tue',
					'close_at_tue',
					'open_at_wed',
					'close_at_wed',
					'open_at_thu',
					'close_at_thu',
					'open_at_fri',
					'close_at_fri',
					'open_at_sat',
					'close_at_sat',
					'open_at_sun',
					'close_at_sun',]
	search_fields = ['name',]


class MealAdmin(admin.ModelAdmin):
	model = Meal
	list_display = ['get_restaurant',
					'meal_name',
					'spicy',
					'price_s',
					'price_m',
					'price_l',]
	search_fields = ['restaurant',
					 'ingredients',
					 'meal_name',
					 'spicy',]

	def get_restaurant(self, obj):
		return restaurant.name
	
	get_restaurant.admin_order_feld = 'meal_name'

'''
class IngredientsAdmin(admin.ModelAdmin):
	model = Ingredients
	list_display = ['ingredient_name',]
	search_fields = ['ingredient_name',]
'''

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Meal, MealAdmin)
#admin.site.register(Ingredients, IngredientsAdmin)

