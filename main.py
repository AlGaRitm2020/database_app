# main.py
from db import * 
from tabulate import tabulate

# escape codes for print
REVESE_COLOR =  "\033[7m"
RESET = "\033[0m"

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
    # check is there such product or not 
    check_query = "SELECT product_name FROM products WHERE product_name = %s;"
    result = execute_query(check_query, (product_name,))
    if len(result) == 0:
        logger.error(f"❌ Product not found: {product_name}")
        logger.info(f"...Printing list of all products...")
        get_list_of_all_products()
        return 0


    # Subquery generates list of vulnerable versions (versions that are in at least 1 vulnerability range)
    # Then, main query select verions, that NOT in this list
    
    query = '''
    SELECT product_name, version
    FROM products 
    WHERE product_name LIKE %s AND version NOT IN 
        (select products.version  
        from products left join vulns on products.product_name = vulns.product_name  
        WHERE (products.product_name LIKE %s)  
        AND (string_to_array(products.version, '.')::int[] >= string_to_array(vulns.start_vuln_version, '.')::int[])  
        AND (string_to_array(products.version, '.')::int[] < string_to_array(vulns.fixed_version, '.')::int[])   
        GROUP BY products.version, products.product_name    
        ORDER BY products.product_name, string_to_array(products.version, '.')::int[])
    


        ;'''


    
    li = execute_query(query, (product_name,product_name))
    print(f"\n{REVESE_COLOR}SAFE versions of {product_name}:{RESET}")
    for row in li:
        print(f"{row['product_name']} {row['version']}")


def get_all_vulns_of_product(product_name, version):
    # check is there such product or not 
    print(product_name, version);
    check_query = "SELECT product_name FROM products WHERE product_name = %s;"
    result = execute_query(check_query, (product_name,))
    if len(result) == 0:
        logger.error(f"❌ Product not found: {product_name}")
        logger.info(f"...Printing list of all products...")
        get_list_of_all_products()
        return 0

    check_query = "SELECT version FROM products WHERE product_name = %s AND version = %s;"
    result = execute_query(check_query, (product_name, version))
    if len(result) == 0:
        logger.error(f"❌ Version not found: {product_name} {version}")
        logger.info(f"...Printing all versions of {product_name}...")
        get_versions_of_product(product_name)
        return 0



    # Subquery generates list of vulnerable versions (versions that are in at least 1 vulnerability range)
    # Then, main query select verions, that NOT in this list
    
    query = '''
        select vulns.vuln_id, vulns.kla_id, vulns.description, vulns.publish_date, vulns.start_vuln_version, vulns.fixed_version 
        from products left join vulns on products.product_name = vulns.product_name  
        WHERE (products.product_name LIKE %s) AND (products.version LIKE %s)   
        AND (string_to_array(products.version, '.')::int[] >= string_to_array(vulns.start_vuln_version, '.')::int[])  
        AND (string_to_array(products.version, '.')::int[] < string_to_array(vulns.fixed_version, '.')::int[])   
        ORDER BY string_to_array(products.version, '.')::int[] ;
        '''


    
    li = execute_query(query, (product_name,version))
    print(f"{REVESE_COLOR}All vulnerabilities of {product_name} {version}:{RESET}")
    # print("KLA_ID  | description | publish data\t| start_vuln_version\t| fixed_version\t ")
    # print("-"*50)
    
    print(tabulate(li, headers='keys', tablefmt='pipe'))
    # lii = [i.values() for i in li]
    # print(lii)

    # for row in li:
    #
    #     kla, desc, pub, start, fix = (row['kla_id'], row['description'], row['publish_date'], row['start_vuln_version'], row['fixed_version'])
    #     print(f'{kla} | {desc}\t\t\t\t| {pub}\t\t| {start}\t\t| {fix}\t\t')
        # print(f"{kla} | '{row['description']}'\t| {row['publish_date']}\t| {row['start_vuln_version']}\t| {row['fixed_version']}\t")


    pass

def get_list_of_all_products():
    query = "select DISTINCT product_name from products;"
    li = execute_query(query)

    print("List of all products: ")
    for row in li:
        print(f"- {row['product_name']}")



def get_versions_of_product(product_name):
    query = "SELECT version FROM products WHERE product_name = %s;"
    li = execute_query(query, (product_name,))

    print(f"Versions of {product_name}: ")
    for row in li:
        print(f"- {row['version']}")
 
def get_versions_between(kla_id):
    query = "SELECT product_name, version FROM products JOIN;"
    li = execute_query(query, (product_name,))

    print(f"Versions of {product_name}: ")
    for row in li:
        print(f"- {row['version']}"+'\t'*2)       


def main():
    init_db()

    show_menu()
    # get_save_versions_of_product("PuTTY")
    # get_versions_of_product("PuTTY - -- DROP TABLE products;")
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
