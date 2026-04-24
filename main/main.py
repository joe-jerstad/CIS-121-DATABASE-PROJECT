import helpers

def main():
    store = helpers.models.Store()
    helpers.load(store)
    while True:
        helpers.clear()
        helpers.header("CIS 121 DBMS")

        choice = helpers.choose(["Product Menu", "Customer Menu", "Order Menu", "Exit Program"])
        if choice == 1:
            helpers.product_menu(store)
        elif choice == 2:
            helpers.customer_menu(store)
        elif choice == 3:
            helpers.order_menu(store)
        elif choice == 4:
            helpers.clear()
            print('Thank you for using CIS 121 DBMS')
            helpers.pause()
            break

if __name__ == "__main__":
    main()