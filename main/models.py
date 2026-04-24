def fixed(data, width: int): #UI helper for formatting things with a max width
    s = str(data)
    return f"{s[:width]:<{width}}"

class Product:
    def __init__(self, product_id: int, name: str, price: float, category: str):
        self.product_id = int(product_id)
        self.name = str(name)
        self.price = float(price)
        self.category = str(category)

    def get_id(self): #additional getter to make store mehod next_id universal
        return self.product_id

    def get_product_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_category(self):
        return self.category

    def __str__(self):
        price_str = f"{self.price:.2f}"
        return f"{fixed(self.product_id, 10)}|{fixed(self.name, 12)}|${fixed(price_str, 11)}|{fixed(self.category, 12)}"
    
    def to_csv_line(self):
        return f"{self.product_id},{self.name},{self.price:.2f},{self.category}"
    
class Customer:
    def __init__(self, customer_id: int, first_name: str, last_name: str, email: str, zip_code: str):
        self.customer_id = int(customer_id)
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.email = str(email)
        self.zip_code = str(zip_code)

    def get_id(self): #additional getter to make store mehod next_id universal
        return self.customer_id

    def get_customer_id(self):
        return self.customer_id

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_zip_code(self):
        return self.zip_code

    def __str__(self):
        return f"{fixed(self.customer_id, 11)}|{fixed(f"{self.last_name}, {self.first_name}", 22)}| {fixed(self.email, 22)} |{fixed(self.zip_code, 8)}"
    
    def to_csv_line(self):
        return f"{self.customer_id},{self.first_name},{self.last_name},{self.email},{self.zip_code}"
    
class Order:
    def __init__(self, order_id: int, customer_id: int, order_date: str):
        self.order_id = int(order_id)
        self.customer_id = int(customer_id)
        self.order_date = str(order_date)
        
    def get_id(self): #additional getter to make store mehod next_id universal
        return self.order_id
    
    def get_order_id(self):
        return self.order_id

    def get_customer_id(self):
        return self.customer_id

    def get_order_date(self):
        return self.order_date
    
    def __str__(self):
        return f"{fixed(self.order_id, 8)}|{fixed(self.customer_id, 11)}|{fixed(self.order_date, 10)}"

    def to_csv_line(self):
        return f"{self.order_id},{self.customer_id},{self.order_date}"

class OrderItem:
    def __init__(self, item_id: int, order_id: int, product_id: int, quantity: int, price: float):
        self.item_id = int(item_id)
        self.order_id = int(order_id)
        self.product_id = int(product_id)
        self.quantity = int(quantity)
        self.price = price
        self.total_price = round(self.quantity * float(price), 2)

    def get_id(self): #additional getter to make store mehod next_id universal
        return self.item_id

    def get_item_id(self):
        return self.item_id

    def get_order_id(self):
        return self.order_id

    def get_product_id(self):
        return self.product_id

    def get_quantity(self):
        return self.quantity
    
    def get_price(self):
        return self.price

    def get_total_price(self):
        return self.total_price
    
    def set_quantity(self, new_quantity):
        self.quantity = new_quantity
        self.total_price = round(new_quantity * float(self.price), 2)

    def __str__(self):
        total_str = f"{self.total_price:.2f}"
        return f"{fixed(self.item_id, 7)}|{fixed(self.order_id, 8)}|{fixed(self.product_id, 10)}|{fixed(self.quantity, 8)}|${fixed(total_str, 11)}"

    def to_csv_line(self):
        return f"{self.item_id},{self.order_id},{self.product_id},{self.quantity},{self.total_price}"

class Store:
    def __init__(self):
        self.products = []
        self.customers = []
        self.orders = []
        self.order_items = []

    #====================Product Methods====================

    def get_products(self):
        return self.products
    
    def add_product(self, product: Product):
        self.products.append(product)

    def edit_product(self, i: int, edited_product: Product):
        self.products[i] = edited_product

    def remove_product(self, product: Product):
        self.products.remove(product)
    
    #====================Customer Methods====================
    
    def get_customers(self):
        return self.customers
    
    def add_customer(self, customer: Customer):
        self.customers.append(customer)

    def edit_customer(self, i: int, edited_customer: Customer):
        self.customers[i] = edited_customer

    def remove_customer(self, customer: Customer):
        self.customers.remove(customer)

    #====================Order Methods====================

    def get_orders(self):
        return self.orders
    
    def add_order(self, order: Order):
        self.orders.append(order)

    def edit_order(self, i: int, edited_order: Order):
        self.orders[i] = edited_order

    def remove_order(self, order: Order):
        self.orders.remove(order)

    #====================Order Item Methods====================
    
    def get_order_items(self):
        return self.order_items
    
    def add_order_item(self, order_item: OrderItem):
        self.order_items.append(order_item)

    def remove_order_item(self, order_item: OrderItem):
        self.order_items.remove(order_item)

    def next_id(self, category: list): #returns the next number 1 higher than the previous highest id 
        ids = []
        for item in category:
            ids.append(item.get_id())
        if ids:
            return max(ids) + 1
        return 1
    
    


    
