import psycopg2
from connect import connect

def add_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "CALL upsert_contacts(%s, %s)", (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

def insert_many_contacts():
    conn = connect()
    cur = conn.cursor()

    names = input("Enter names separated by comma: ").split(",")
    phones = input("Enter phones separated by comma: ").split(",")

    cur.execute(
        "CALL insert_many(%s, %s)",
        (names, phones)
    )
    conn.commit()

    cur.execute(
        "SELECT * FROM invalid_contacts"
    )
    invalid_rows = cur.fetchall()
    if invalid_rows:
        print("\nInvalid contacts found:")
        for name, phone in invalid_rows:
            print(f"Name: {name}, Phone: {phone}")
        
        cur.execute("TRUNCATE TABLE invalid_contacts")
        conn.commit()
    else:
        print("All contacts inserted successfully!")

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
        "SELECT * FROM search_contacts(%s)", (keyword,)
    )

    print(cur.fetchall())

    cur.close()
    conn.close()


def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    if value.lower() == "all":
        cur.execute(
            "TRUNCATE TABLE contacts RESTART IDENTITY"
        )
    else:
        cur.execute(
        "CALL delete_contact(%s)",
        (value,)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    print(cur.fetchall())

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
        print("\n1 Add/Update")
        print("2 Show")
        print("3 Search")
        print("4 Paginate")
        print("5 Delete")
        print("6 Import CSV")
        print("7 Bulk insert")
        print("0 Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact(input("Name: "), input("Phone: "))

        elif choice == "2":
            get_contacts()

        elif choice == "3":
            search_contacts(input("Search: "))

        elif choice == "4":
            get_paginated(input("How many records: "), input("From which position: "))

        elif choice == "5":
            delete_contact(input("Name or phone or all: "))

        elif choice == "6":
            import_csv()

        elif choice == "7":
            insert_many_contacts()

        elif choice == "0":
            break

if __name__ == "__main__":
    menu()