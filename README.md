# Hospital System - Python OOP Prototype

## Project Idea

This project is a simple console hospital system made with Python OOP.

There are two types of users:

- Patient
- Doctor

The main goal is to let a patient book an appointment with a doctor, then allow the doctor to add radiology, medical tests, medicines, and follow-up visits.

The system also supports Undo for data-changing actions.

---

## Patient Profile

A patient enters:

- Name
- Phone
- Address
- Supported company or not
- Chronic diseases
- Password

If the patient works for a supported company:

- Appointment is free
- Diagnostic radiology is free
- Medical tests are free
- Medicines still have their normal price

---

## Doctor Profile

A doctor enters:

- Name
- Phone
- Address
- National ID
- Syndicate ID
- Specialty
- Password

The doctor can add available days and times.

---

## Main Classes

### User

Abstract parent class.

Children:

- Patient
- Doctor

It also uses a private password and private phone number.

### Patient

Stores patient information and has a MedicalRecord.

### Doctor

Stores doctor information and available dates/times.

### MedicalItem

Abstract parent class.

Children:

- Radiology
- MedicalTest
- Medicine

### MedicalRecord

Stores:

- Radiology
- Medical tests
- Medicines
- Results

### Appointment

Connects a patient and doctor.

### FollowUp

Stores follow-up information.

### HospitalSystem

Controls the whole program.

It stores:

- Patients
- Doctors
- Appointments
- Follow-ups
- Undo history

---

## OOP Concepts Used

### 1. Abstraction

The program uses:

```python
class User(ABC)
```

and:

```python
class MedicalItem(ABC)
```

with `@abstractmethod`.

---

### 2. Encapsulation

The User class has private attributes:

```python
self.__phone
self.__password
```

It also uses `@property` for the phone number.

---

### 3. Inheritance

First inheritance relationship:

```text
User
├── Patient
└── Doctor
```

Second inheritance relationship:

```text
MedicalItem
├── Radiology
├── MedicalTest
└── Medicine
```

---

### 4. Polymorphism

`show_info()` works differently in Patient and Doctor.

`get_patient_price()` also works differently.

For example:

- Radiology is free for a supported patient.
- Medical tests are free for a supported patient.
- Medicine keeps its normal price.

---

### 5. Python-Style Overloading

Doctor availability uses `*times`.

Example:

```python
doctor.add_availability("2026-09-01", "10:00")
```

or:

```python
doctor.add_availability(
    "2026-09-01",
    "10:00",
    "11:00",
    "12:00"
)
```

---

### 6. Association

Appointment connects:

```text
Patient <-> Appointment <-> Doctor
```

---

### 7. Aggregation

HospitalSystem stores Patient and Doctor objects.

---

### 8. Composition

Every Patient creates its own MedicalRecord.

```python
self.medical_record = MedicalRecord()
```

---

## Patient Functions

Patient can:

- Create profile
- Login
- View profile
- View doctors
- View doctor available times
- Book appointment
- View appointments
- View follow-ups
- View radiology/tests/medicines
- See prices
- Add radiology/test results
- Cancel appointment
- Change phone
- Undo last action

---

## Doctor Functions

Doctor can:

- Create profile
- Login
- View profile
- Add available times
- Remove available times
- View upcoming appointments
- Open an appointment
- See patient data
- Add radiology
- Add medical tests
- Add medicines
- Edit medical items
- Remove medical items
- Add follow-up
- Mark appointment as completed
- View follow-ups
- Open follow-up
- See patient data
- See radiology/test results
- Add/edit/remove items during follow-up
- Change phone
- Undo last action

---

## Undo

Before an important change, the system saves a copy of its current data.

Example:

```text
Medicine price = 100
Doctor changes it to 150
Undo
Medicine price returns to 100
```

The program uses:

```python
deepcopy()
```

to save the old state.

This is simple enough for a student prototype.

---

## How to Run

You need Python 3.

Open the project folder and run:

```bash
python hospital_system_simple.py
```

---
