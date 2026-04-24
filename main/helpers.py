import os
import models
from datetime import datetime

#====================FILE HANDLING====================

def load(store: models.Store):
    """Loads every csv file into the database management program"""
    load_products(store)
    load_customers(store)
    load_orders(store)
    load_order_items(store)

def load_products(store: models.Store):
    if not os.path.exists('products.csv'):
        open('products.csv', 'w').close()
        return

    products = open('products.csv','r')

    for line in products.readlines()[1:]:
        attributes = line.strip().split(',')
        store.add_product(models.Product(int(attributes[0]), attributes[1], float(attributes[2]), attributes[3]))
    
    products.close()

def load_customers(store: models.Store):
    if not os.path.exists('customers.csv'):
        open('customers.csv', 'w').close()
        return
    
    customers = open('customers.csv', 'r')

    for line in customers.readlines()[1:]:
        attributes = line.strip().split(',')
        store.add_customer(models.Customer(int(attributes[0]), attributes[1], attributes[2], attributes[3], attributes[4]))
    
    customers.close()

def load_orders(store: models.Store):
    if not os.path.exists('orders.csv'):
        open('orders.csv', 'w').close()
        return
    
    orders = open('orders.csv', 'r')

    for line in orders.readlines()[1:]:
        attributes = line.strip().split(',')
        store.add_order(models.Order(int(attributes[0]), int(attributes[1]), attributes[2]))

    orders.close()

def load_order_items(store: models.Store):
    if not os.path.exists('order_items.csv'):
        open('order_items.csv', 'w').close()
        return
    
    order_items = open('order_items.csv', 'r')

    for line in order_items.readlines()[1:]:
        attributes = line.strip().split(',')
        quantity = int(attributes[3])
        total_price = float(attributes[4])
        price = round(total_price / quantity, 2)
        store.add_order_item(models.OrderItem(int(attributes[0]),int(attributes[1]), int(attributes[2]), quantity, price)  )

        order_items.close()

def save_products(store: models.Store):
    products = open('products.csv','w')

    products.write('product id,name,price,category\n')
    for product in store.get_products():
        products.write(f"{product.to_csv_line()}\n")

    products.close()

def save_customers(store: models.Store):
    customers = open('customers.csv', 'w')

    customers.write('customer id,first name,last name,email,zip code\n')
    for customer in store.get_customers():
        customers.write(f"{customer.to_csv_line()}\n")

    customers.close()

def save_orders(store: models.Store):
    orders = open('orders.csv', 'w')

    orders.write('order id,customer id,date\n')
    for order in store.get_orders():
        orders.write(f"{order.to_csv_line()}\n")

    orders.close()

def save_order_items(store: models.Store):
    order_items = open('order_items.csv', 'w')

    order_items.write('item id,order id,product id,quantity,total price\n')
    for order_item in store.get_order_items():
        order_items.write(f"{order_item.to_csv_line()}\n")
    
    order_items.close()

#====================UI HELPERS====================

def header(title: str):
    """Formatting for the headers of each section"""
    print('=' * 40)
    print(f"    {title}")
    print('=' * 40)

def clear():
    """Clears out the terminal for a cleaner UI"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pause():
    """Lets the user stay on whatever they are viewing until they enter something"""
    input("\nPress enter to continue...")

def choose(options: list):
    """Used for menu options to confirm that they are entering a valid selection, takes a list of 
    options as an argument and returns the integer option they selected"""
    for i, option in enumerate(options, 1):
        print(f"{i} - {option}")
    print()

    while True:
        try:
            selection = int(input("Selection: "))
        except ValueError:
            print("\nInvalid Entry - Enter a number from the list.\n")
        else:
            if selection >= 1 and selection <= len(options):
                return selection
            else:
                print("\nInvalid Entry - Enter a number from the list.\n")

order_item_header = "Item ID|Order ID|Product ID|Quantity|Total Price "

order_header = "Order ID|Customer ID|Date      "

product_header = "Product ID|Name        |Price       |Category    "

customer_header = "Customer ID|Name                  |Email                   |Zip Code"

#====================Other Helpers====================

#====================Product Menu====================

def product_menu(store: models.Store):
    while True:
        clear()
        header("PRODUCT MENU")

        choice = choose(["View All", "Create", "Edit", "Delete", "Exit to Main Menu"])
        if choice == 1:
            view_products(store)
        elif choice == 2:
            create_product(store)
        elif choice == 3:
            edit_product(store)
        elif choice == 4:
            delete_product(store)
        elif choice == 5:
            save_products(store)
            break

def view_products(store: models.Store):
    clear()
    header("VIEW PRODUCTS")

    if store.get_products(): #checks if there are any available products in the store
        print(product_header)
        for product in store.get_products():
            print(product)
    else:
        print("There are currently no products available to view.")
    pause()

def create_product(store: models.Store):
    clear()
    header("CREATE PRODUCT")
    print('*Required Field\n')

    product_id = store.next_id(store.get_products()) #generates the next id as one higher number than the highest id

    while True:
        name = input("Product name*: ")
        if name != '': #if they enter any name we can continue
            break
        else:
            print("\nInvalid Entry - You must enter a product name.\n")

    while True:
        try:
            price = float(input("Price*: "))
        except ValueError:
            print('\nInvalid Entry - You must enter a number to represent the price of the product.\n')
        else:
            if price >= 0.01:
                price = round(price, 2) #rounds the price to 2 decimals
                break
            else:
                print("\nInvalid Entry - Price must be a positive number.\n")

    category = input("Category (optional): ") #category is not required and can be inputted as ''

    store.add_product(models.Product(product_id, name, price, category))

    print(f'\nProduct "{name}" successfully created with ID [{product_id}]')
    pause()

def edit_product(store: models.Store):
    clear()
    header("EDIT PRODUCTS")

    if store.get_products():
        print(product_header)
        for product in store.get_products(): #print out the products available to edit if there are products
            print(product)
        print()
    else:
        print("There are currently no products available to edit.")
        pause()
        return
    
    valid_ids = [] #create a list of the ids that are available for a user to select from
    for product in store.get_products():
        valid_ids.append(product.get_product_id())
    
    while True:
        try:
            choice = input("Enter the ID of the product you would like to edit or press enter to cancel: ")
            if choice == '': #if the user presses enter they will be broken out of the loop and stop editing orders
                break
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - You must enter a product ID from the list.\n")
        else:
            if choice in valid_ids: #confirms that the choice selected is a valid entry in the list of products
                for ind, product in enumerate(store.get_products()):
                    if choice == product.get_product_id():
                        i = ind #converts the users choice into the index connected to the product in the store

                new_name = input(f"Name ({store.get_products()[i].get_name()}): ")
                if new_name == '': #if the user doesn't enter a new name, the old name is used instead
                    new_name = store.get_products()[i].get_name()
                
                while True:
                    try:
                        new_price = input(f"Price ({store.get_products()[i].get_price()}): ")
                        if new_price == '': #if the user doesn't enter a new price, the old price is used
                            new_price = store.get_products()[i].get_price()
                            break
                        else: 
                            new_price = float(new_price) #trys to convert the new price to a float
                    except ValueError:
                        print('\nInvalid Entry - You must enter a number to represent the price of the product.\n')
                    else:
                        if new_price >= 0.01:
                            new_price = round(new_price, 2) #rounds the price to 2 decimals
                            break
                        else:
                            print("\nInvalid Entry - Price must be a positive number.\n")
            
                new_category = input(f"Category ({store.get_products()[i].get_category()}): ")
                if new_category == '': #if a new category is not entered, the old category is used
                    new_category = store.get_products()[i].get_category()
                
                clear()
                header("CONFIRM CHANGES")
                print(f"{product_header}\n{store.get_products()[i]}\n\nWill change to:\n\n{product_header}\n{models.Product(choice, new_name, new_price, new_category)}")

                while True:
                    confirm = input(f"\nConfirm changes (y/n): ").lower()
                    if confirm == 'y':
                        store.edit_product(i, models.Product(choice, new_name, new_price, new_category)) #replaces the product at the selected index with the new product attributes
                        print(f"\nProduct [{choice}] successfully edited.")
                        pause()
                        break
                    elif confirm == 'n':
                        print("\nProduct changes not saved.")
                        pause()
                        break
                    else:
                        print('\nInvalid Entry - Enter either "y" or "n".\n')
                break
            else:
                print("\nInvalid Entry - You must enter a product ID from the list.\n")

def delete_product(store: models.Store):
    clear()
    header("DELETE PRODUCTS")

    if store.get_products():
        print(product_header)
        for product in store.get_products(): #print out the products available to edit if there are products
            print(product)
        print()
    else:
        print("There are currently no products available to delete.")
        pause()
        return #exit the deleting menu if there are no products
    
    valid_ids = [] #create a list of available ids the user can select
    for product in store.get_products():
        valid_ids.append(product.get_product_id())

    while True:
        try:
            choice = (input("Enter the ID of the product you would like to delete or press enter to cancel: "))
            if choice == '': #if the user presses enter, they will exit the deleting menu
                break
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - Enter an available product ID or cancel.\n")
        else:
            if choice in valid_ids: #check if the choice is one of the available options
                for product in store.get_products():
                    if choice == product.get_product_id(): #match the users choice with the product they want to delete
                        clear()
                        header("CONFIRM PRODUCT DELETE")
                        print(f"Are you sure you want to delete:\n{product_header}\n{product}")

                        while True:
                            confirm = input(f"\nConfirm deletion (y/n): ").lower()
                            if confirm == 'y':
                                store.remove_product(product) #delete the product from the store class
                                print(f"\nProduct [{choice}] successfully deleted.")
                                pause()
                                break
                            elif confirm == 'n':
                                print(f"\nProduct [{choice}] not deleted.")
                                pause()
                                break
                            else:
                                print('\nInvalid Entry - Enter either "y" or "n".\n')
                        break 
                break 
            else: #make sure the users choice is within the available ids
                print('\nInvalid Entry - Enter an available product ID or cancel.\n') 

#====================Customer Menu====================

def customer_menu(store: models.Store):
    while True:
        clear()
        header("CUSTOMER MENU")

        choice = choose(["View All", "Create", "Edit", "Delete", "Exit to Main Menu"])
        if choice == 1:
            view_customers(store)
        elif choice == 2:
            create_customer(store)
        elif choice == 3:
            edit_customer(store)
        elif choice == 4:
            delete_customer(store)
        elif choice == 5:
            save_customers(store)
            break

def view_customers(store: models.Store):
    clear()
    header("VIEW CUSTOMERS")

    if store.get_customers(): #checks if there are any customers in the store
        print(customer_header)
        for customer in store.get_customers():
            print(customer)
    else:
        print("There are currently no customers available to view.")
    pause()

def create_customer(store: models.Store):
    clear()
    header("CREATE CUSTOMER")
    print('*Required Field\n')

    customer_id = store.next_id(store.get_customers()) #gets the next available id and assigns it to customer

    while True:
        first_name = input('First name*: ')
        if first_name != '': #the user can continue if they enter a first name
            break
        else:
            print("\nInvalid Entry - You must enter a first name for the customer.\n")
    
    while True:
        last_name = input("Last name*: ")
        if last_name != '': #the user can continue if they enter a last name
            break
        else:
            print("\nInvalid Entry - You must enter a last name for the customer.\n")
    
    while True:
        email = input("Email*: ")
        if email != '': #user cannot skip email creation
            if '@' in email: #if @ is in the email, it is valid
                break
            else:
                print("\nInvalid Entry - Email address must include the @ symbol.\n")
        else:
            print('\nInvalid Entry - You must enter an email address.\n')

    while True:
        zip_code = input("Zip code (optional): ")
        if zip_code == '': #allows user to skip zip code
            break
        else:
            if zip_code.isdigit() and len(zip_code) == 5: #checks if the zip code is a 5 digit number
                break
            else:
                print("\nInvalid Entry - Zip code must be a 5 digit number.\n")
    
    store.add_customer(models.Customer(customer_id, first_name, last_name, email, zip_code))

    print(f'\nCustomer "{last_name}, {first_name}" successfully created with ID [{customer_id}]')
    pause()

def edit_customer(store: models.Store):
    clear()
    header("EDIT CUSTOMER")

    if store.get_customers():
        print(customer_header)
        for customer in store.get_customers():
            print(customer)
        print()
    else:
        print("There are no customers available to edit.")
        pause()
        return
    
    valid_ids = []
    for customer in store.get_customers():
        valid_ids.append(customer.get_customer_id())

    while True:
        try:
            choice = input("Enter the ID of the customer you would like to edit or press enter to exit: ") #if user presses enter the loop is broken
            if choice == '':
                break
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - You must enter a customer ID from the list.\n")
        else:
            if choice in valid_ids:
                for ind, customer in enumerate(store.get_customers()):
                    if choice == customer.get_customer_id():
                        i = ind

                new_first = input(f"First name ({store.get_customers()[i].get_first_name()}): ")
                if new_first == '': #if the user leaves the section blank, use the current first name
                    new_first = store.get_customers()[i].get_first_name()
                
                new_last = input(f"Last ({store.get_customers()[i].get_last_name()}): ")
                if new_last == '':
                    new_last = store.get_customers()[i].get_last_name()

                while True:
                    new_email = input(f"Email ({store.get_customers()[i].get_email()}): ")
                    if new_email == '':
                        new_email = store.get_customers()[i].get_email()
                        break
                    elif '@' in new_email:
                        break
                    else:
                        print("\nInvalid Entry - Email must contain the @ symbol.\n")
                
                while True:
                    new_zip_code = input(f"Zip code ({store.get_customers()[i].get_zip_code()}): ")
                    if new_zip_code == '':
                        new_zip_code = store.get_customers()[i].get_zip_code()
                        break
                    elif new_zip_code.isdigit() and len(new_zip_code) == 5:
                        break
                    else:
                        print("\nInvalid Entry - Zip code must be a 5 digit number.\n")
                
                clear()
                header("CONFIRM CHANGES")
                print(f"{customer_header}\n{store.get_customers()[i]}\n\nWill change to:\n\n{customer_header}\n{models.Customer(choice, new_first, new_last, new_email, new_zip_code)}")

                while True:
                    confirm = input(f"\nConfirm changes (y/n): ").lower()
                    if confirm == 'y':
                        store.edit_customer(i, models.Customer(choice, new_first, new_last, new_email, new_zip_code)) #replaces the customer at the selected index with the new customer attributes
                        print(f"\nCustomer [{choice}] successfully edited.")
                        pause()
                        break
                    elif confirm == 'n':
                        print("\nCustomer changes not saved.")
                        pause()
                        break
                    else:
                        print('\nInvalid Entry - Enter either "y" or "n".\n')
                break

            else:
                print("\nInvalid Entry - You must enter a customer ID from the list.\n")

def delete_customer(store):
    clear()
    header("DELETE CUSTOMER")

    if store.get_customers():
        print(customer_header)
        for customer in store.get_customers():
            print(customer)
        print()
    else:
        print("There are currently no customers available to delete.")
        pause()
        return
    
    valid_ids = []
    for customer in store.get_customers():
        valid_ids.append(customer.get_customer_id())

    while True:
        try:
            choice = input("Enter the ID of the customer you would like to delete or press enter to cancel: ")
            if choice == '':
                break
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - Enter an available customer ID or cancel.\n")
        else:
            if choice in valid_ids: #checcks if user choice is in the list of ids
                for customer in store.get_customers():
                    if choice == customer.get_customer_id():
                        clear()
                        header("CONFIRM CUSTOMER DELETE")
                        print(f"Are you sure you want to delete:\n{customer_header}\n{customer}")

                        while True:
                            confirm = input(f"\nConfirm deletion (y/n): ").lower()
                            if confirm == 'y':
                                store.remove_customer(customer) #delete the customer from the store class
                                print(f"\nCustomer [{choice}] successfully deleted.")
                                pause()
                                break
                            elif confirm == 'n':
                                print(f"\nCustomer [{choice}] not deleted.")
                                pause()
                                break
                            else:
                                print('\nInvalid Entry - Enter either "y" or "n".\n')
                        break
                break
            else:
                print("\nInvalid Entry - Enter an available customer ID or cancel.\n")
                    
#====================Order Menu====================

def order_menu(store: models.Store):
    while True:
        clear()
        header("ORDER MENU")

        choice = choose(["View All", "Create", "Edit", "Delete", "Exit to Main Menu"])
        if choice == 1:
            view_orders(store)
        elif choice == 2:
            create_order(store)
        elif choice == 3:
            edit_order(store)
        elif choice == 4:
            delete_order(store)
        elif choice == 5:
            save_orders(store)
            save_order_items(store)
            break

def view_orders(store: models.Store):
    clear()
    header("VIEW ORDERS")

    if store.get_orders(): #checks if there are any orders in the store
        print(order_header)
        for order in store.get_orders():
            print(order)
        print()

    else:
        print("There are currently no orders available to view.")
        pause()
        return

    valid_ids = [] #create a list of available ids
    for order in store.get_orders():
        valid_ids.append(order.get_order_id())

    while True:
        try:
            choice = input("Enter the ID to view order details or press enter to cancel: ")
            if choice == '': #if user presses enter, stops viewing the orders
                break
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - Enter an available order ID or cancel.\n")
        else:
            if choice in valid_ids:
                clear()
                header(f"VIEWING ORDER [{choice}]")

                print(order_item_header)
                for order_item in store.get_order_items():
                    if order_item.get_order_id() == choice:
                        print(order_item)
                pause()
                break
            else:
                print("\nInvalid Entry - Enter an available order ID or cancel.\n")

def create_order(store: models.Store):
    clear()
    header("CREATE ORDER")
    print('*Required Field\n')

    if not store.get_customers(): #confirms there are customers available
        print("There must be existing customers to create an order.")
        pause()
        return

    if not store.get_products(): #confirms there are products available
        print("There must be existing products to create an order.")
        pause()
        return        

    order_id = store.next_id(store.get_orders()) #gets the next avaialble id for the order

    while True:
        order_date = input("Order date* (MM/DD/YYYY): ")
        if order_date == '':
            print("\nInvalid Entry - You must enter an order date.\n")
        else:
            try:
                datetime.strptime(order_date, '%m/%d/%Y') #makes sure the date is valid and in the correct format
                break
            except ValueError:
                print("\nInvalid Entry - Date must be in MM/DD/YYYY format.\n")

    valid_customer_ids = [] #makes a list of avbailable customer ids
    for customer in store.get_customers():
        valid_customer_ids.append(customer.get_customer_id())

    clear()
    header("CUSTOMER SELECTION")

    print(customer_header)
    for customer in store.get_customers():
        print(customer)
    print()

    while True:
        try:
            customer_id = input("Enter a customer ID from the list of customers or press enter to cancel: ")
            if customer_id == '':
                return #cancel creation if they press enter
            else:
                customer_id = int(customer_id)
        except ValueError:
            print("\nInvalid Entry - Enter a customer ID from the list or cancel.\n")
        else:
            if customer_id in valid_customer_ids:
                break #if the id is valid, keep that customer ID
            else:
                print("\nInvalid Entry - Enter a customer ID from the list or cancel.\n")

    clear()
    header("SELECT PRODUCT")

    item_id = store.next_id(store.get_order_items()) #gets the next available item id

    valid_product_ids = [] #creates a list of available product ids
    for product in store.get_products():
        valid_product_ids.append(product.get_product_id())

    remaining_products = [] #creates a list of products available
    for product in store.get_products():
        remaining_products.append(product)

    print(product_header)
    for product in remaining_products:
        print(product)
    print()

    while True:
        try:
            choice = input("Enter the product ID you would like to add to the order or press enter to cancel: ")
            if choice == '': #allows them to cancel creating the order
                return
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - You must enter a product ID from the list or cancel.\n")
        else:
            if choice in valid_product_ids:
                product_id = choice
                valid_product_ids.remove(product_id) #the used product id is no longer valid
                for product in remaining_products:
                    if product.get_product_id() == product_id: 
                        remaining_products.remove(product) #removes the product from the list when used in the order
                break
            else:
                print("\nInvalid Entry - You must enter a product ID from the list or cancel.\n")

    while True:
        try:
            quantity = int(input("Quantity*: "))
        except ValueError:
            print("\nInvalid Entry - You must enter a number for the quantity.\n")
        else:
            if quantity > 0:
                break
            else:
                print("\nInvalid Entry - You must enter a positive value for quantity.\n")

    for product in store.get_products():
        if product.get_product_id() == product_id:
            price = product.get_price() #gets the price related to the product to calculate total price of the item in the order

    store.add_order(models.Order(order_id, customer_id, order_date)) 

    store.add_order_item(models.OrderItem(item_id, order_id, product_id, quantity, price))

    while True:
        another = input("\nWould you like to add another product (y/n)?: ")
        if another == 'y':
            clear()
            header("SELECT PRODUCT")

            item_id = store.next_id(store.get_order_items())

            if not remaining_products: #if there are no products available, finish the creation
                print("There are no products remaining to add.")
                pause()
                return

            print(product_header)
            for product in remaining_products:
                print(product)
            print()

            while True:
                try:
                    choice = input("Enter the product ID you would like to add to the order or press enter to cancel: ")
                    if choice == '':
                        return
                    else:
                        choice = int(choice)
                except ValueError:
                    print("\nInvalid Entry - You must enter a product ID from the list or cancel.\n")
                else:
                    if choice in valid_product_ids:
                        product_id = choice
                        valid_product_ids.remove(product_id)
                        for product in remaining_products:
                            if product.get_product_id() == product_id:
                                remaining_products.remove(product)
                        break
                    else:
                        print("\nInvalid Entry - You must enter a product ID from the list or cancel.\n")

            while True:
                try:
                    quantity = int(input("Quantity*: "))
                except ValueError:
                    print("\nInvalid Entry - You must enter a number for the quantity.\n")
                else:
                    if quantity > 0:
                        break
                    else:
                        print("\nInvalid Entry - You must enter a positive value for quantity.\n")

            for product in store.get_products():
                if product.get_product_id() == product_id:
                    price = product.get_price()

            store.add_order_item(models.OrderItem(item_id, order_id, product_id, quantity, price))

        elif another == 'n':
            return
        else:
            print('\nInvalid Entry - Enter "y" or "n".\n')

def delete_order(store: models.Store):
    clear()
    header("DELETE ORDER")

    if store.get_orders():
        print(order_header)
        for order in store.get_orders():
            print(order)
        print()
    else:
        print("There are currently no orders available to delete.")
        pause()
        return

    valid_ids = []
    for order in store.get_orders():
        valid_ids.append(order.get_order_id())
    
    while True:
        try:
            choice = input("Enter the ID of the order you would like to delete or press enter to cancel: ")
            if choice == '':
                break
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - Enter an available order ID or cancel.\n")
        else:
            if choice in valid_ids:
                for order in store.get_orders():
                    if choice == order.get_order_id():
                        clear()
                        header("CONFIRM ORDER DELETE")
                        print(f"Are you sure you want to delete:\n{order_header}\n{order}")
                        print(f"\nIt will also delete the order items:\n{order_item_header}")
                        for order_item in store.get_order_items():
                            if order_item.get_order_id() == choice:
                                print(order_item)
                        print()

                        while True:
                            confirm = input(f"\nConfirm deletion (y/n): ").lower()
                            if confirm == 'y':
                                store.remove_order(order) #delete the order from the store class
                                items_to_remove = []
                                for order_item in store.get_order_items():
                                    if order_item.get_order_id() == choice:
                                        items_to_remove.append(order_item)

                                for order_item in items_to_remove:
                                    store.remove_order_item(order_item)

                                print(f"\nOrder [{choice}] successfully deleted.")
                                pause()
                                break
                            elif confirm == 'n':
                                print(f"\nOrder [{choice}] not deleted.")
                                pause()
                                break
                            else:
                                print('\nInvalid Entry - Enter either "y" or "n".\n')
                        break
                break
            else:
                print("\nInvalid Entry - Enter an available order ID or cancel.\n")
                            
def edit_order_details(store: models.Store):
    clear()
    header("EDIT ORDER DETAILS")

    print(order_header)
    for order in store.get_orders():
        print(order)
    print()

    valid_ids = []
    for order in store.get_orders():
        valid_ids.append(order.get_order_id())

    while True:
        try:
            choice = input("Enter the order you would like to edit or press enter to cancel: ")
            if choice == '':
                break
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - You must enter on of the IDs from the list or cancel.\n")
        else:
            if choice in valid_ids:
                for ind, order in enumerate(store.get_orders()):
                    if choice == order.get_order_id():
                        i = ind

                while True:
                        new_date = input(f"Date ({store.get_orders()[i].get_order_date()}): ")
                        if new_date == '':
                            new_date = store.get_orders()[i].get_order_date()
                            break
                        else:
                            try:
                                datetime.strptime(new_date, '%m/%d/%Y') #makes sure the date is valid and in the correct format
                                break
                            except ValueError:
                                print("\nInvalid Entry - Date must be in MM/DD/YYYY format.\n")
                
                valid_customer_ids = []
                for customer in store.get_customers():
                    valid_customer_ids.append(customer.get_customer_id())
                
                clear()
                header("CUSTOMER SELECTION")

                print(customer_header)
                for customer in store.get_customers():
                    print(customer)
                print()

                while True:
                    try:
                        new_customer_id = input(f"Customer ID ({store.get_orders()[i].get_customer_id()}): ")
                        if new_customer_id == '':
                            new_customer_id = store.get_orders()[i].get_customer_id()
                            break
                        else:
                            new_customer_id = int(new_customer_id)
                    except ValueError:
                        print("\nInvalid Entry - Enter a customer ID from the list.\n")
                    else:
                        if new_customer_id in valid_customer_ids:
                            break #if the id is valid, keep that customer ID
                        else:
                            print("\nInvalid Entry - Enter a customer ID from the list.\n")

                clear()
                header("CONFIRM CHANGES")
                print(f"{order_header}\n{store.get_orders()[i]}\n\nWill change to:\n\n{order_header}\n{models.Order(choice, new_customer_id, new_date)}")

                while True:
                    confirm = input(f"\nConfirm changes (y/n): ").lower()
                    if confirm == 'y':
                        store.edit_order(i, models.Order(choice, new_customer_id, new_date)) #replaces the order at the selected index with the new order attributes
                        print(f"\nOrder [{choice}] successfully edited.")
                        pause()
                        break
                    elif confirm == 'n':
                        print("\nOrder changes not saved.")
                        pause()
                        break
                    else:
                        print('\nInvalid Entry - Enter either "y" or "n".\n')                
                break
            else:
                print("\nInvalid Entry - You must enter on of the IDs from the list or cancel.\n")       

def add_order_item(store: models.Store, order_id: int):
    clear()
    header(f"ADD ITEM TO ORDER [{order_id}]")

    item_id = store.next_id(store.get_order_items())

    used_product_ids = []
    available_product_ids = []

    for order_item in store.get_order_items():
        if order_item.get_order_id() == order_id:
            used_product_ids.append(order_item.get_product_id())

    for product in store.get_products():
        if product.get_product_id() not in used_product_ids:
            available_product_ids.append(product.get_product_id())

    if available_product_ids:
        print(product_header)
        for product in store.get_products():
            if product.get_product_id() in available_product_ids:
                print(product)
        print()

        while True:
            try:
                choice = input("Enter the product ID you would like to add to the order or press enter to cancel: ")
                if choice == '': #allows them to cancel creating the order
                    return
                else:
                    choice = int(choice)
            except ValueError:
                print("\nInvalid Entry - You must enter a product ID from the list or cancel.\n")
            else:
                if choice in available_product_ids:
                    product_id = choice
                    available_product_ids.remove(product_id) #the used product id is no longer valid
                    break
                else:
                    print("\nInvalid Entry - You must enter a product ID from the list or cancel.\n")

        while True:
            try:
                quantity = int(input("Quantity*: "))
            except ValueError:
                print("\nInvalid Entry - You must enter a number for the quantity.\n")
            else:
                if quantity > 0:
                    break
                else:
                    print("\nInvalid Entry - You must enter a positive value for quantity.\n")

        for product in store.get_products():
            if product.get_product_id() == product_id:
                price = product.get_price() #gets the price related to the product to calculate total price of the item in the order

        
        store.add_order_item(models.OrderItem(item_id, order_id, product_id, quantity, price))
    else:
        print("There are no additional products to be added to this order.")
        pause()
        return

def edit_item_quantity(store: models.Store, order_id: int):
    clear()
    header(f"EDIT ITEM QUANTITY FOR [{order_id}]")

    valid_item_ids = []

    print(order_item_header)
    for order_item in store.get_order_items():
        if order_item.get_order_id() == order_id:
            valid_item_ids.append(order_item.get_item_id())
            print(order_item)

    while True:
        try:
            choice = input("\nEnter the ID of the item you would like to edit or press enter to cancel: ")
            if choice == '':
                return
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - You must pick an item ID from the list or cancel.\n")
        else:
            if choice in valid_item_ids:
                for order_item in store.get_order_items():
                    if choice == order_item.get_item_id():
                        while True:
                            try:
                                new_quantity = input(f"Quantity ({order_item.get_quantity()}): ")
                                if new_quantity == '':
                                    new_quantity = order_item.get_quantity()
                                else:
                                    new_quantity = int(new_quantity)
                            except ValueError:
                                print("\nInvalid Entry - You must enter a number for the quantity.\n")
                            else:
                                if new_quantity > 0:
                                    break
                                else:
                                    print("\nInvalid Entry - You must enter a positive value for quantity.\n")

                        clear()
                        header("CONFIRM CHANGES")
                        print(f"{order_item_header}\n{order_item}\n\nWill change to:\n\n{order_item_header}\n{models.OrderItem(choice, order_item.get_order_id(), order_item.get_product_id(), new_quantity, order_item.get_price())}")

                        while True:
                            confirm = input(f"\nConfirm changes (y/n): ").lower()
                            if confirm == 'y':
                                order_item.set_quantity(new_quantity) #sets the new quantity
                                print(f"\nOrder Item [{choice}] successfully edited.")
                                pause()
                                break
                            elif confirm == 'n':
                                print("\nOrder Item changes not saved.")
                                pause()
                                break
                            else:
                                print('\nInvalid Entry - Enter either "y" or "n".\n')
                break
            else:
                print("\nInvalid Entry - You must pick an item ID from the list or cancel.\n")
        
def delete_order_item(store: models.Store, order_id: int):
    clear()
    header(f"DELETE ITEM FROM [{order_id}]")

    current_item_ids = []

    print(order_item_header)
    for order_item in store.get_order_items():
        if order_item.get_order_id() == order_id:
            print(order_item)
            current_item_ids.append(order_item.get_item_id())

    if len(current_item_ids) < 2:
        print(f"\nThere is only 1 item in order [{order_id}], you cannot have an order without items.")
        pause()
        return
    
    while True:
        try:
            choice = input("\nEnter the ID of the item you would like to delete or press enter to cancel: ")
            if choice == '':
                return
            else:
                choice = int(choice)
        except ValueError:
            print("\nInvalid Entry - You must pick an item ID from the list or cancel.\n")
        else:
            if choice in current_item_ids:
                for order_item in store.get_order_items():
                    if choice == order_item.get_item_id():
                        clear()
                        header("CONFIRM ITEM DELETE")
                        print(f"Are you sure you want to delete item:\n{order_item_header}\n{order_item}")

                        while True:
                            confirm = input(f"\nConfirm deletion (y/n): ").lower()
                            if confirm == 'y':
                                store.remove_order_item(order_item) #delete the order item from the store class
                                print(f"\nOrder item [{choice}] successfully deleted.")
                                pause()
                                break
                            elif confirm == 'n':
                                print(f"\nOrder item [{choice}] not deleted.")
                                pause()
                                break
                            else:
                                print('\nInvalid Entry - Enter either "y" or "n".\n')
                break
            else:
                print("\nInvalid Entry - You must pick an item ID from the list or cancel.\n")

def edit_order_items(store: models.Store):
    clear()
    header("EDIT ORDER ITEMS")

    print(order_header)
    for order in store.get_orders():
        print(order)
    print()

    valid_ids = []
    for order in store.get_orders():
        valid_ids.append(order.get_order_id())

    while True:
            choice = input("Enter the ID of the order you would like to edit or press enter to cancel: ")
            try:
                if choice == '':
                    break
                else:
                    choice = int(choice)
            except ValueError:
                print("\nInvalid Entry - Enter an ID from the list or press enter to cancel\n")
            else:
                if choice in valid_ids:
                    clear()
                    header(f"EDITING ITEMS FROM ORDER [{choice}]")

                    menu_choice = choose(["Add order item", "Edit Item Quantity", "Delete Order Item", "Cancel"])
                    if menu_choice == 1:
                        add_order_item(store, choice)
                        break
                    if menu_choice == 2:
                        edit_item_quantity(store, choice)
                        break
                    if menu_choice == 3:
                        delete_order_item(store, choice)
                        break
                    if menu_choice == 4:
                        break
                        
def edit_order(store: models.Store):
    clear()
    header("EDIT ORDER MENU")

    if not store.get_orders():
        print("There are currently no orders available to edit.")
        pause()
        return
    
    choice = choose(["Edit Order Details", "Edit Order Items", "Cancel"])
    if choice == 1:
        edit_order_details(store)
        
    elif choice == 2:
        edit_order_items(store)

    elif choice == 3:
        return