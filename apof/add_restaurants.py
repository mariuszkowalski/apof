# -*- coding: utf-8 -*-
from django.db import models
from models import Restaurant, Meal, Ingredients


r1 = Restaurant(name='Coloseum',
				phone='(67) 352 91 11',
				open_at_mon='12:00',
				close_at_mon='22:00',
				open_at_tue='11:00',
				close_at_tue='22:00',
				open_at_wed='11:00',
				close_at_wed='22:00',
				open_at_thu='11:00',
				close_at_thu='22:00',
				open_at_fri='11:00',
				close_at_fri='23:00',
				open_at_sat='11:00',
				close_at_sat='23:00',
				open_at_sun='12:00',
				close_at_sun='22:00')
r1.save()

#r1 = Restaurant(name='Coloseum', phone='(67) 352 91 11', open_at_mon='12:00', close_at_mon='22:00', open_at_tue='11:00', close_at_tue='22:00', open_at_wed='11:00', close_at_wed='22:00', open_at_thu='11:00', close_at_thu='22:00', open_at_fri='11:00', close_at_fri='23:00', open_at_sat='11:00', close_at_sat='23:00', open_at_sun='12:00', close_at_sun='22:00')