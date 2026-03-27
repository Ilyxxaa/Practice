import psycopg2
from connect import connect

def add_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

def get_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def search_contacts(keyword):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE name ILIKE %s OR phone LIKE %s",
        (f"%{keyword}%", f"{keyword}%") #finding all similarities with our prefix %""% - anywhere inside, ""% starting with our prefix
    )

    print(cur.fetchall())

    cur.close()
    conn.close()

def update_contact(name, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE contacts SET name=%s WHERE name=%s",
            (new_name, name)
        )

    if new_phone:
        cur.execute(
            "UPDATE contacts SET phone=%s WHERE name=%s",
            (new_phone, name)
        )

    conn.commit()
    cur.close()
    conn.close()

def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s OR phone=%s",
        (value, value)
    )
    if value == "ALL" or "All" or "all":
        cur.execute(
            "TRUNCATE TABLE contacts"
        )

    conn.commit()
    cur.close()
    conn.close()

#----------------------------------------------------------------------------------------
# Import from csv file into SQL
import csv

def import_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )
        
    conn.commit()
    cur.close()
    conn.close()

#----------------------------------------------------------------------------------------
# The menu

def menu():
    while True:
        print("\n1 Add")
        print("2 Show")
        print("3 Search")
        print("4 Update")
        print("5 Delete")
        print("6 Import CSV")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact(input("Name: "), input("Phone: "))

        elif choice == "2":
            get_contacts()

        elif choice == "3":
            search_contacts(input("Search: "))

        elif choice == "4":
            name = input("Old name: ")
            new_name = input("New name: ")
            new_phone = input("New phone: ")
            update_contact(name, new_name or None, new_phone or None)

        elif choice == "5":
            delete_contact(input("Name or phone or all: "))

        elif choice == "6":
            import_csv()

        elif choice == "0":
            break

if __name__ == "__main__":
    menu()