# main.py
from db import * 

def show_menu():
    print("\n" + "="*40)
    print("CLI application to work with DB")
    print("="*40)
    print("OPTTIONS:")

    print("list - Get list of all products")
    print("safe - Get safe versions of product")
    print("vuln - Get all vulnerabilities of product ")
    print("load - load tables from json")
    print("help - show menu")
    print("quit - Close application")
    print("-"*40)

def get_save_versions_of_product(product_name):
    pass

def get_all_vulns_of_product(product_name, version):
    pass

def get_list_of_all_products():
    query = "select DISTINCT product_name from products;"
    di = execute_query(query)

    print("List of all products: ")
    for j in di:
        print(f"- {j['product_name']}"+'\t'*2)



def main():
    init_db()

    show_menu()
    while True:
        choice = input("DBapp >> ").strip()

        if choice == "safe":
            product_name = input("Enter product name: ").strip()
            get_save_versions_of_product(product_name)
        elif choice == "vuln":
            product_name = input("Enter product name: ").strip()
            version = input("Enter product version: ").strip()
            get_all_vulns_of_product(product_name, version)           

        elif choice == "load":
            import_vulnerabilities('data/vulnerabilities.json')
            import_products('data/versions.json')

        elif choice == "list":
            get_list_of_all_products()
        elif choice == "help":
            show_menu()
        elif choice == "quit":
            print("Bye!")
            break
        else:
            print("❗Wrong option. Try again.")

if __name__ == "__main__":
    main()
