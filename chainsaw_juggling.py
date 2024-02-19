"""
A menu - you need to add the database and fill in the functions. 
"""
import sqlite3


# TODO create database table OR set up Peewee model to create table

def main():
    # Create table if is not exists
    with sqlite3.connect('records_db.sqlite') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS records (name text unique, country text, catches int)')

    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    conn = sqlite3.connect('records_db.sqlite')
    results = conn.execute('SELECT * FROM records')
    print('Display all records: ')
    for row in results:
        print(row)  # each row is a table
    conn.close()


def search_by_name():
    """" Asks user for a name, and print the matching record if found.
     What should the program do if the name is not found?' """

    name = input('Enter the name: ')
    conn = sqlite3.connect('records_db.sqlite')
    results = conn.execute('SELECT * FROM records WHERE name like ?', (name,))
    first_row = results.fetchall()  # fetchone() returns Non if rows found

    if first_row:
        print('You are: ', first_row)
    else:
        print('Name Not Found')
    conn.close()


def add_new_record():
    # add a record if is not already exists
    name = input('Enter the name of the new record: ')
    country = input('Enter the new country: ')
    catches = int(input('How many catches: '))
    with sqlite3.connect('records_db.sqlite') as conn:
        try:
            conn.execute('INSERT INTO records VALUES (?,?,?)', (name, country, catches))
            print('The record added into the data.')
        except sqlite3.IntegrityError:  # This catches if the record is already in the database
            print('This record is already in the database.')
    conn.close()


def edit_existing_record():
    # edit existing record. What if user wants to edit record that does not exist?'

    name = input('Enter the name of the record want to edit: ')
    update_record = int(input('What is ' + name + '\'s new record? '))
    conn = sqlite3.connect('records_db.sqlite')
    results = conn.execute('SELECT * FROM records WHERE name like ?', (name,))
    first_row = results.fetchone()  # fetchone() returns Non if rows found

    if first_row:
        conn.execute('UPDATE records SET catches = ? WHERE UPPER(name) = UPPER(?) ', (update_record, name))
        conn.commit()
        print('The record was updated successfully')
    else:
        print('The record not found.')

    conn.close()


def delete_record():
    # print('todo delete existing record. What if user wants to delete record that does not exist?')
    name = input('Enter name of the record to delete: ')
    with sqlite3.connect('records_db.sqlite') as conn:
        deleted_record = conn.execute('DELETE FROM records WHERE UPPER(name) = UPPER(?)', (name,))
        rows_affected = deleted_record.rowcount  # This will show how many rows were affected/deleted
    conn.close()

    if rows_affected == 0:  # if no record were deleted
        print('\n The name ' + name + ' was not found')
    else:
        print(name + ' was deleted')


if __name__ == '__main__':
    main()
