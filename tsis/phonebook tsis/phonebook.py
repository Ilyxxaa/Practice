import csv
import json
from datetime import datetime
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

from connect import connect

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = BASE_DIR / "schema.sql"
PROCEDURES_FILE = BASE_DIR / "procedures.sql"
CSV_FILE = BASE_DIR / "contacts.csv"
EXPORT_FILE = BASE_DIR / "contacts_export.json"

VALID_PHONE_TYPES = {"home", "work", "mobile"}
VALID_SORT_FIELDS = {
    "name": "c.name",
    "birthday": "c.birthday",
    "date": "c.created_at"
}


def run_sql_file(path):
    """Runs a .sql file in PostgreSQL."""
    conn = connect()
    cur = conn.cursor()
    with open(path, "r", encoding="utf-8") as file:
        cur.execute(file.read())
    conn.commit()
    cur.close()
    conn.close()


def setup_database():
    """Creates/updates tables and installs stored procedures/functions."""
    run_sql_file(SCHEMA_FILE)
    run_sql_file(PROCEDURES_FILE)
    print("Database schema and procedures are ready.")


def get_or_create_group(cur, group_name):
    """Returns group id. Creates the group if it does not exist."""
    group_name = (group_name or "Other").strip() or "Other"
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def normalize_phone_type(phone_type):
    """Makes sure phone type is one of: home, work, mobile."""
    phone_type = (phone_type or "mobile").strip().lower()
    if phone_type not in VALID_PHONE_TYPES:
        phone_type = "mobile"
    return phone_type


def add_contact(name, phone=None, phone_type="mobile", email=None, birthday=None, group_name="Other"):
    """
    Adds a contact with extended fields.
    A contact can have many phones, so phone is inserted into the phones table.
    """
    conn = connect()
    cur = conn.cursor()

    group_id = get_or_create_group(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts (name, email, birthday, group_id)
        VALUES (%s, %s, NULLIF(%s, '')::DATE, %s)
        ON CONFLICT (name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (name, email or None, birthday or "", group_id)
    )
    contact_id = cur.fetchone()[0]

    if phone:
        cur.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (contact_id, phone) DO UPDATE
            SET type = EXCLUDED.type
            """,
            (contact_id, phone, normalize_phone_type(phone_type))
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact saved.")


def print_contacts(rows):
    """Pretty console output for contact rows."""
    if not rows:
        print("No contacts found.")
        return

    print("\nID | Name | Email | Birthday | Group | Phones | Created")
    print("-" * 90)
    for row in rows:
        print(
            f"{row['contact_id']} | {row['name']} | {row.get('email') or '-'} | "
            f"{row.get('birthday') or '-'} | {row.get('group_name') or '-'} | "
            f"{row.get('phones') or '-'} | {row.get('created_at') or '-'}"
        )


def get_contacts(sort_by="name", group_filter=None, limit=None, offset=0):
    """
    Shows contacts with optional group filter, sorting, and pagination.
    sort_by can be: name, birthday, date.
    """
    sort_sql = VALID_SORT_FIELDS.get(sort_by, "c.name")

    query = f"""
        SELECT
            c.id AS contact_id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.type, p.phone), '') AS phones,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
    """
    params = []

    if group_filter:
        query += " WHERE g.name ILIKE %s"
        params.append(group_filter)

    query += f" GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at ORDER BY {sort_sql} NULLS LAST"

    if limit is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    print_contacts(rows)
    return rows


def search_contacts_console(keyword):
    """
    Uses the new PostgreSQL function search_contacts().
    It searches name, email, group, and all phone numbers.
    """
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM search_contacts(%s)", (keyword,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    print_contacts(rows)


def search_by_email(email_part):
    """Searches contacts by partial email match."""
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT
            c.id AS contact_id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE c.email ILIKE %s
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY c.name
        """,
        (f"%{email_part}%",)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    print_contacts(rows)


def update_contact(name, new_name=None, new_email=None, new_birthday=None, new_group=None):
    """Updates contact main fields. Phone numbers are managed separately."""
    conn = connect()
    cur = conn.cursor()

    fields = []
    params = []

    if new_name:
        fields.append("name = %s")
        params.append(new_name)
    if new_email is not None:
        fields.append("email = %s")
        params.append(new_email or None)
    if new_birthday is not None:
        fields.append("birthday = NULLIF(%s, '')::DATE")
        params.append(new_birthday)
    if new_group:
        group_id = get_or_create_group(cur, new_group)
        fields.append("group_id = %s")
        params.append(group_id)

    if not fields:
        print("Nothing to update.")
        cur.close()
        conn.close()
        return

    params.append(name)
    cur.execute(f"UPDATE contacts SET {', '.join(fields)} WHERE name = %s", params)

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")


def delete_contact(value):
    """Deletes contact by name or by any phone number. Type ALL to clear all tables."""
    conn = connect()
    cur = conn.cursor()

    if value.lower() == "all":
        cur.execute("TRUNCATE TABLE phones, contacts RESTART IDENTITY CASCADE")
        print("All contacts deleted.")
    else:
        cur.execute(
            """
            DELETE FROM contacts
            WHERE name = %s
               OR id IN (SELECT contact_id FROM phones WHERE phone = %s)
            """,
            (value, value)
        )
        print("Contact deleted if it existed.")

    conn.commit()
    cur.close()
    conn.close()


def add_phone_to_contact(contact_name, phone, phone_type):
    """Calls the PostgreSQL procedure add_phone()."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, normalize_phone_type(phone_type)))
    conn.commit()
    cur.close()
    conn.close()
    print("Phone added.")


def move_contact_to_group(contact_name, group_name):
    """Calls the PostgreSQL procedure move_to_group()."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact moved to group.")


def import_csv(path=CSV_FILE):
    """
    Imports contacts from CSV.
    Supports both old format:
        name, phone
    and new format with headers:
        name, phone, phone_type, email, birthday, group
    """
    path = Path(path)
    if not path.exists():
        print(f"CSV file not found: {path}")
        return

    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        sample = file.read(2048)
        file.seek(0)
        has_header = csv.Sniffer().has_header(sample)

        if has_header:
            reader = csv.DictReader(file)
            for row in reader:
                add_contact(
                    row.get("name", "").strip(),
                    row.get("phone", "").strip(),
                    row.get("phone_type", "mobile").strip(),
                    row.get("email", "").strip(),
                    row.get("birthday", "").strip(),
                    row.get("group", "Other").strip()
                )
        else:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    add_contact(row[0].strip(), row[1].strip(), "mobile", None, None, "Other")

    print("CSV import finished.")


def export_json(path=EXPORT_FILE):
    """Exports all contacts with phones and groups to JSON."""
    conn = connect()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            c.created_at,
            g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.name
        """
    )
    contacts = cur.fetchall()

    for contact in contacts:
        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY type, phone",
            (contact["id"],)
        )
        contact["phones"] = cur.fetchall()
        contact["birthday"] = str(contact["birthday"]) if contact["birthday"] else None
        contact["created_at"] = str(contact["created_at"]) if contact["created_at"] else None

    cur.close()
    conn.close()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    print(f"Exported to {path}")


def contact_exists(name):
    """Checks duplicate by contact name."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists


def import_json(path=EXPORT_FILE):
    """
    Imports contacts from JSON.
    If contact with same name exists, asks: skip or overwrite.
    """
    path = Path(path)
    if not path.exists():
        print(f"JSON file not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    for contact in contacts:
        name = contact.get("name", "").strip()
        if not name:
            continue

        if contact_exists(name):
            answer = input(f"Contact '{name}' exists. Skip or overwrite? [s/o]: ").strip().lower()
            if answer != "o":
                print("Skipped.")
                continue
            delete_contact(name)

        phones = contact.get("phones") or []
        first_phone = phones[0] if phones else {}

        add_contact(
            name=name,
            phone=first_phone.get("phone"),
            phone_type=first_phone.get("type", "mobile"),
            email=contact.get("email"),
            birthday=contact.get("birthday"),
            group_name=contact.get("group_name") or "Other"
        )

        for phone in phones[1:]:
            add_phone_to_contact(name, phone.get("phone"), phone.get("type", "mobile"))

    print("JSON import finished.")


def paginated_navigation():
    """Console page navigation: next / prev / quit."""
    page_size = int(input("Page size: ") or "5")
    sort_by = input("Sort by name/birthday/date: ") or "name"
    group_filter = input("Group filter, empty for all: ").strip() or None
    page = 0

    while True:
        print(f"\nPage {page + 1}")
        rows = get_contacts(sort_by=sort_by, group_filter=group_filter, limit=page_size, offset=page * page_size)

        command = input("next / prev / quit: ").strip().lower()
        if command == "next":
            if rows:
                page += 1
        elif command == "prev":
            page = max(0, page - 1)
        elif command == "quit":
            break


def menu():
    """Main console menu."""
    while True:
        print("\n--- Extended PhoneBook ---")
        print("1  Setup database")
        print("2  Add contact")
        print("3  Show contacts")
        print("4  Search all fields")
        print("5  Search by email")
        print("6  Filter by group")
        print("7  Update contact")
        print("8  Delete contact")
        print("9  Add phone to contact")
        print("10 Move contact to group")
        print("11 Import CSV")
        print("12 Export JSON")
        print("13 Import JSON")
        print("14 Paginated navigation")
        print("0  Exit")

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                setup_database()

            elif choice == "2":
                add_contact(
                    name=input("Name: "),
                    phone=input("Phone: "),
                    phone_type=input("Phone type home/work/mobile: "),
                    email=input("Email: "),
                    birthday=input("Birthday YYYY-MM-DD, empty if none: "),
                    group_name=input("Group: ")
                )

            elif choice == "3":
                sort_by = input("Sort by name/birthday/date: ") or "name"
                get_contacts(sort_by=sort_by)

            elif choice == "4":
                search_contacts_console(input("Search: "))

            elif choice == "5":
                search_by_email(input("Email contains: "))

            elif choice == "6":
                get_contacts(group_filter=input("Group name: "))

            elif choice == "7":
                old_name = input("Current name: ")
                update_contact(
                    name=old_name,
                    new_name=input("New name, empty skip: ") or None,
                    new_email=input("New email, empty clears/skips depending on input: "),
                    new_birthday=input("New birthday YYYY-MM-DD, empty clears/skips depending on input: "),
                    new_group=input("New group, empty skip: ") or None
                )

            elif choice == "8":
                delete_contact(input("Name, phone, or ALL: "))

            elif choice == "9":
                add_phone_to_contact(
                    input("Contact name: "),
                    input("Phone: "),
                    input("Type home/work/mobile: ")
                )

            elif choice == "10":
                move_contact_to_group(input("Contact name: "), input("New group: "))

            elif choice == "11":
                path = input("CSV path, empty for contacts.csv: ").strip() or CSV_FILE
                import_csv(path)

            elif choice == "12":
                path = input("JSON export path, empty for contacts_export.json: ").strip() or EXPORT_FILE
                export_json(path)

            elif choice == "13":
                path = input("JSON import path, empty for contacts_export.json: ").strip() or EXPORT_FILE
                import_json(path)

            elif choice == "14":
                paginated_navigation()

            elif choice == "0":
                break

        except psycopg2.Error as error:
            print("Database error:", error)
        except ValueError as error:
            print("Input error:", error)


if __name__ == "__main__":
    menu()
