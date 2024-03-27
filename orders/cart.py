from home.models import Product


CART_SESSION_ID = 'cart'  # name session

class Cart:
	def __init__(self, request):
		self.session = request.session  # get all sessions that in request
		cart = self.session.get(CART_SESSION_ID)
		if not cart:
			cart = self.session[CART_SESSION_ID] = {}
		self.cart = cart

	def __iter__(self):
		product_ids = self.cart.keys()  # get all id
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()  # take a copy of user cart
		for product in products:
			cart[str(product.id)]['product'] = product

		for item in cart.values():
			item['total_price'] = int(item['price']) * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def add(self, product, quantity):   # this method add product to cart
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity':0, 'price':str(product.price)}
		self.cart[product_id]['quantity'] += quantity
		self.save()  # call method save this class

	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def save(self):
		self.session.modified = True

	def get_total_price(self):
		return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		del self.session[CART_SESSION_ID]
		self.save()
