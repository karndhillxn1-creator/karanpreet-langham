"""
File name: langham_hotel_management.py
Description: Console-based LANGHAM Hotel Management System for BBIM502 Assessment 2.
Author: Karanpreet Singh
Date: 2025-11-06

Educational example: review, understand, test, and adapt this code yourself.
"""

from datetime import datetime
from pathlib import Path
import shutil
import sys

DATA_FILE = Path("LHMS_850009690.txt")  # Replace Studentid with your actual ID.
ROOMS = {}
ALLOCATIONS = {}
NEXT_ALLOCATION_ID = 1

ROOM_TYPES = {
    "Single": 100.00,
    "Double": 150.00,
    "Deluxe": 220.00,
    "Suite": 350.00,
}


def read_int(prompt, minimum=None):
    """Read an integer safely, optionally enforcing a minimum."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Please enter a number greater than or equal to {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")
        except EOFError:
            print("\nInput ended. Returning to the menu.")
            return None


def read_nonempty(prompt):
    """Read a non-empty text value."""
    while True:
        try:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty.")
        except EOFError:
            print("\nInput ended. Returning to the menu.")
            return None


def add_rooms():
    """Menu 1: Add rooms to the hotel inventory."""
    count = read_int("How many rooms would you like to add? ", 1)
    if count is None:
        return
    for _ in range(count):
        room_number = read_nonempty("Room number: ")
        if room_number is None:
            return
        if room_number in ROOMS:
            print("That room number already exists; this room was skipped.")
            continue

        print("Room types:", ", ".join(ROOM_TYPES))
        while True:
            room_type_value = read_nonempty("Room type: ")
            if room_type_value is None:
                return
            room_type = room_type_value.title()
            if room_type in ROOM_TYPES:
                break
            print("Invalid room type. Please choose from:",
                  ", ".join(ROOM_TYPES))

        capacity = read_int("Maximum guests: ", 1)
        if capacity is None:
            return
        ROOMS[room_number] = {
            "type": room_type,
            "capacity": capacity,   
            "rate": ROOM_TYPES[room_type],
            "available": True,
        }
        print(f"Room {room_number} added successfully.")
    save_data(silent=True)


def delete_rooms():
    """Menu 2: Delete an unallocated room."""
    room_number = read_nonempty("Room number to delete: ")
    if room_number is None:
        return
    if room_number not in ROOMS:
        print("Room not found.")
    elif not ROOMS[room_number]["available"]:
        print("This room is currently allocated and cannot be deleted.")
    else:
        del ROOMS[room_number]
        print(f"Room {room_number} deleted.")
        save_data(silent=True)


def display_rooms():
    """Menu 3: Display room features and availability."""
    if not ROOMS:
        print("No rooms have been added yet.")
        return
    print("\nROOM INVENTORY")
    print("-" * 66)
    print(f"{'Room':<10}{'Type':<15}{'Capacity':<12}{'Rate/night':<15}{'Status'}")
    print("-" * 66)
    for number, room in sorted(ROOMS.items()):
        status = "Available" if room["available"] else "Allocated"
        print(f"{number:<10}{room['type']:<15}{room['capacity']:<12}{room['rate']:<15.2f}{status}")
    print("-" * 66)


def allocate_room():
    """Menu 4: Allocate an available room to a customer."""
    available = [n for n, r in ROOMS.items() if r["available"]]
    if not available:
        print("There are no available rooms.")
        return
    display_rooms()
    room_number = read_nonempty("Room number to allocate: ")
    if room_number is None:
        return
    if room_number not in ROOMS:
        print("Room not found.")
        return
    if not ROOMS[room_number]["available"]:
        print("That room is already allocated.")
        return

    customer = read_nonempty("Customer full name: ")
    if customer is None:
        return
    nights = read_int("Number of nights: ", 1)
    if nights is None:
        return
    guests = read_int("Number of guests: ", 1)
    if guests is None:
        return
    if guests > ROOMS[room_number]["capacity"]:
        print(f"This room accommodates up to {ROOMS[room_number]['capacity']} guests.")
        return

    global NEXT_ALLOCATION_ID
    allocation_id = NEXT_ALLOCATION_ID
    NEXT_ALLOCATION_ID += 1
    allocation = {
        "id": allocation_id,
        "room": room_number,
        "customer": customer,
        "nights": nights,
        "guests": guests,
        "rate": ROOMS[room_number]["rate"],
        "allocated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    ALLOCATIONS[allocation_id] = allocation
    ROOMS[room_number]["available"] = False
    print(f"Booking confirmed. Allocation ID: {allocation_id}")
    print(f"Estimated total: ${allocation['rate'] * nights:.2f}")
    save_data(silent=True)


def display_allocations():
    """Menu 5: Display current room allocation details."""
    current = [a for a in ALLOCATIONS.values() if a["room"] in ROOMS and not ROOMS[a["room"]]["available"]]
    if not current:
        print("There are no current room allocations.")
        return
    print("\nCURRENT ROOM ALLOCATIONS")
    print("-" * 90)
    print(f"{'ID':<6}{'Room':<10}{'Customer':<24}{'Nights':<10}{'Guests':<10}{'Rate/night':<12}{'Total'}")
    print("-" * 90)
    for a in current:
        total = a["nights"] * a["rate"]
        print(f"{a['id']:<6}{a['room']:<10}{a['customer'][:23]:<24}{a['nights']:<10}{a['guests']:<10}{a['rate']:<12.2f}${total:.2f}")
    print("-" * 90)


def billing_and_deallocate():
    """Menu 6: Generate bill and release a room."""
    display_allocations()
    allocation_id = read_int("Allocation ID to check out: ", 1)
    if allocation_id is None:
        return
    allocation = ALLOCATIONS.get(allocation_id)
    if allocation is None:
        print("Allocation ID not found.")
        return

    subtotal = allocation["rate"] * allocation["nights"]
    # Illustrative GST calculation; confirm the rate/approach expected by your tutor.
    gst = subtotal * 0.15
    total = subtotal + gst
    print("\nLANGHAM HOTELS - CUSTOMER BILL")
    print(f"Customer: {allocation['customer']}")
    print(f"Room: {allocation['room']} | Nights: {allocation['nights']}")
    print(f"Room charges: ${subtotal:.2f}")
    print(f"GST (15%): ${gst:.2f}")
    print(f"Total due: ${total:.2f}")

    confirm = read_nonempty("Confirm payment and release room? (yes/no): ").lower()
    if confirm is None:
        return
    if confirm == "yes":
        ROOMS[allocation["room"]]["available"] = True
        del ALLOCATIONS[allocation_id]
        print("Payment recorded (demo). Room released for the next booking.")
        save_data(silent=True)
    else:
        print("Checkout cancelled; allocation remains active.")


def serialised_data():
    """Return a readable text representation of room and allocation data."""
    lines = [
        "LANGHAM HOTEL MANAGEMENT SYSTEM",
        f"Saved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "ROOMS:"
    ]
    for number, room in sorted(ROOMS.items()):
        lines.append(
            f"Room={number}|Type={room['type']}|Capacity={room['capacity']}|"
            f"Rate={room['rate']:.2f}|Available={room['available']}"
        )
    lines += ["", "ALLOCATIONS:"]
    for a in ALLOCATIONS.values():
        lines.append(
            f"ID={a['id']}|Room={a['room']}|Customer={a['customer']}|"
            f"Nights={a['nights']}|Guests={a['guests']}|Rate={a['rate']:.2f}|"
            f"Allocated={a['allocated_at']}"
        )
    return "\n".join(lines) + "\n"


def save_data(silent=False):
    """Menu 7: Save current application data to the text file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            file.write(serialised_data())
        if not silent:
            print(f"Room and allocation data saved to {DATA_FILE}.")
    except OSError as error:
        print(f"File could not be saved: {error}")


def display_file():
    """Menu 8: Read and display saved data."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            content = file.read()
        print("\nSAVED ROOM ALLOCATION FILE")
        print("-" * 50)
        print(content if content.strip() else "(The file is empty.)")
        print("-" * 50)
    except FileNotFoundError:
        print(f"{DATA_FILE} does not exist. Use option 7 to save first.")
    except OSError as error:
        print(f"Unable to read the file: {error}")


def backup_and_clear_file():
    """Menu 9: Append saved data to a timestamped backup, then clear original."""
    try:
        if not DATA_FILE.exists():
            print(f"{DATA_FILE} does not exist. Use option 7 to save first.")
            return
        content = DATA_FILE.read_text(encoding="utf-8")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = DATA_FILE.with_name(f"{DATA_FILE.stem}_Backup_{timestamp}.txt")
        with backup_file.open("a", encoding="utf-8") as file:
            file.write(content)
            file.write("\n" + "=" * 60 + "\n")
        DATA_FILE.write_text("", encoding="utf-8")
        print(f"Backup created: {backup_file}")
        print(f"Original file {DATA_FILE} has been cleared.")
    except OSError as error:
        print(f"Backup/clear operation failed: {error}")


def show_menu():
    """Display the application menu."""
    print("\n" + "*" * 56)
    print("          LANGHAM HOTEL MANAGEMENT SYSTEM")
    print("*" * 56)
    print("1. Add Rooms")
    print("2. Delete Rooms")
    print("3. Display Rooms Details")
    print("4. Allocate Rooms")
    print("5. Display Room Allocation Details")
    print("6. Billing & De-Allocation")
    print("7. Save Room Allocations to a File")
    print("8. Show Room Allocations from a File")
    print("9. Backup and Clear Room Allocation File")
    print("0. Exit")
    print("*" * 56)


def main():
    """Run the menu loop and dispatch selected operations."""
    actions = {
        1: add_rooms,
        2: delete_rooms,
        3: display_rooms,
        4: allocate_room,
        5: display_allocations,
        6: billing_and_deallocate,
        7: save_data,
        8: display_file,
        9: backup_and_clear_file,
    }
    while True:
        try:
            show_menu()
            choice = read_int("Enter your choice number: ")
            if choice is None:
                continue
            if choice == 0:
                print("Thank you for using LANGHAM Hotel Management System.")
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid menu choice. Please select 0–9.")
        except (KeyboardInterrupt, EOFError):
            print("\nApplication closed safely.")
            break
        except (TypeError, IndexError, ZeroDivisionError, OverflowError) as error:
            print(f"Unexpected input/calculation issue handled: {error}")
        except Exception as error:
            print(f"Unexpected application error: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
