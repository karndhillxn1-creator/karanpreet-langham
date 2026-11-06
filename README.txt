LANGHAM Hotel Management System - BBIM502 Assessment 2

1. Install Python 3 (https://www.python.org/downloads/).
2. Open this folder in VS Code, PyCharm, or a terminal.
3. Replace "Studentid" in DATA_FILE with your actual student ID.
4. Run:
   python langham_hotel_management.py

Testing suggestions:
- Add rooms 101 (Single, capacity 1), 102 (Double, capacity 2), 201 (Suite, capacity 4).
- Display rooms, allocate a room, display allocations, then checkout.
- Save data (option 7), display file (option 8), backup/clear (option 9).
- Try invalid menu input, invalid number input, duplicate room numbers,
  booking an allocated room, and a missing file.

Important:
- This is an educational starter implementation. Read and understand it, test it,
  and adapt it to your instructor's exact expectations before submission.
- Billing uses an illustrative 15% GST calculation; confirm whether your tutor
  expects GST to be included and how it should be calculated.
- The program stores data in memory during a session. File options save a readable
  report; they do not reload room records into memory automatically.
