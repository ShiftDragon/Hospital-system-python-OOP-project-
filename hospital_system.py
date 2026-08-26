from abc import ABC, abstractmethod
from copy import deepcopy


# -------------------------------------------------
# Users
# -------------------------------------------------

class User(ABC):

    def __init__(self, user_id, name, phone, address, password):
        self.user_id = user_id
        self.name = name
        self.__phone = phone
        self.address = address
        self.__password = password

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, new_phone):
        self.__phone = new_phone

    def check_password(self, password):
        return self.__password == password

    @abstractmethod
    def show_info(self):
        pass

# -------------------------------------------------
# Patient
# -------------------------------------------------

class Patient(User):

    def __init__(self, user_id, name, phone, address,
                 supported_company, chronic_diseases, password):

        super().__init__(user_id, name, phone, address, password)

        self.supported_company = supported_company
        self.chronic_diseases = chronic_diseases

        
        self.medical_record = MedicalRecord()

    def show_info(self):
        print("\n--- Patient Data ---")
        print("ID:", self.user_id)
        print("Name:", self.name)
        print("Phone:", self.phone)
        print("Address:", self.address)
        print("Supported company:", self.supported_company)

        if len(self.chronic_diseases) == 0:
            print("Chronic diseases: None")
        else:
            print("Chronic diseases:", ", ".join(self.chronic_diseases))

# -------------------------------------------------
# Doctor
# -------------------------------------------------

class Doctor(User):

    def __init__(self, user_id, name, phone, address,
                 national_id, syndicate_id, specialty, password):

        super().__init__(user_id, name, phone, address, password)

        self.national_id = national_id
        self.syndicate_id = syndicate_id
        self.specialty = specialty

        self.consultation_price = 300

        
        self.available_times = {}

    
    def add_availability(self, date, *times):

        if date not in self.available_times:
            self.available_times[date] = []

        for time in times:
            if time not in self.available_times[date]:
                self.available_times[date].append(time)

    def remove_availability(self, date, time):

        if date in self.available_times:
            if time in self.available_times[date]:

                self.available_times[date].remove(time)

                if len(self.available_times[date]) == 0:
                    del self.available_times[date]

    def is_available(self, date, time):

        if date not in self.available_times:
            return False

        return time in self.available_times[date]

    def show_info(self):
        print("\n--- Doctor Data ---")
        print("ID:", self.user_id)
        print("Name:", self.name)
        print("Phone:", self.phone)
        print("Address:", self.address)
        print("National ID:", self.national_id)
        print("Syndicate ID:", self.syndicate_id)
        print("Specialty:", self.specialty)


# -------------------------------------------------
# Medical items
# -------------------------------------------------

class MedicalItem(ABC):

    def __init__(self, item_id, name, price, appointment_id):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.appointment_id = appointment_id

    @abstractmethod
    def get_type(self):
        pass

    # Default price
    def get_patient_price(self, patient):
        return self.price


class Radiology(MedicalItem):

    def get_type(self):
        return "Diagnostic Radiology"

    
    # Supported-company patients get radiology for free.
    def get_patient_price(self, patient):

        if patient.supported_company:
            return 0

        return self.price


class MedicalTest(MedicalItem):

    def get_type(self):
        return "Medical Test"

    def get_patient_price(self, patient):

        if patient.supported_company:
            return 0

        return self.price


class Medicine(MedicalItem):

    def get_type(self):
        return "Medicine"


# -------------------------------------------------
# Medical Record
# -------------------------------------------------

class MedicalRecord:

    def __init__(self):
        self.items = []
        self.results = {}

    def add_item(self, item):
        self.items.append(item)

    def find_item(self, item_id):

        for item in self.items:
            if item.item_id == item_id:
                return item

        return None

    def remove_item(self, item_id):

        item = self.find_item(item_id)

        if item is not None:
            self.items.remove(item)

            if item_id in self.results:
                del self.results[item_id]

            return True

        return False

    def add_result(self, item_id, result):
        self.results[item_id] = result


# -------------------------------------------------
# Appointment and Follow Up
# -------------------------------------------------

class Appointment:

    
    # Appointment connects a patient and a doctor.
    def __init__(self, appointment_id, patient_id, doctor_id,
                 date, time, price):

        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.price = price
        self.status = "Upcoming"


class FollowUp:

    def __init__(self, follow_up_id, appointment_id,
                 patient_id, doctor_id, date, time):

        self.follow_up_id = follow_up_id
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.status = "Upcoming"


# -------------------------------------------------
# Main Hospital System
# -------------------------------------------------

class HospitalSystem:

    def __init__(self):

        
        # The system stores doctors and patients.
        self.patients = {}
        self.doctors = {}

        self.appointments = {}
        self.follow_ups = {}

        self.next_user_id = 1
        self.next_appointment_id = 1
        self.next_follow_up_id = 1
        self.next_item_id = 1

        self.history = []

    # ----------------------
    # Undo
    # ----------------------

    def save_state(self):

        state = deepcopy([
            self.patients,
            self.doctors,
            self.appointments,
            self.follow_ups,
            self.next_user_id,
            self.next_appointment_id,
            self.next_follow_up_id,
            self.next_item_id
        ])

        self.history.append(state)

    def undo(self):

        if len(self.history) == 0:
            print("Nothing to undo.")
            return

        state = self.history.pop()

        self.patients = state[0]
        self.doctors = state[1]
        self.appointments = state[2]
        self.follow_ups = state[3]
        self.next_user_id = state[4]
        self.next_appointment_id = state[5]
        self.next_follow_up_id = state[6]
        self.next_item_id = state[7]

        print("Last action was undone.")

    # ----------------------
    # Create profiles
    # ----------------------

    def create_patient(self, name, phone, address,
                       supported_company, chronic_diseases, password):

        self.save_state()

        patient = Patient(
            self.next_user_id,
            name,
            phone,
            address,
            supported_company,
            chronic_diseases,
            password
        )

        self.patients[self.next_user_id] = patient

        print("Patient profile created.")
        print("Your ID is:", self.next_user_id)

        self.next_user_id += 1

    def create_doctor(self, name, phone, address,
                      national_id, syndicate_id, specialty, password):

        self.save_state()

        doctor = Doctor(
            self.next_user_id,
            name,
            phone,
            address,
            national_id,
            syndicate_id,
            specialty,
            password
        )

        self.doctors[self.next_user_id] = doctor

        print("Doctor profile created.")
        print("Your ID is:", self.next_user_id)

        self.next_user_id += 1

    # ----------------------
    # Login
    # ----------------------

    def login_patient(self, user_id, password):

        if user_id in self.patients:

            patient = self.patients[user_id]

            if patient.check_password(password):
                return patient

        return None

    def login_doctor(self, user_id, password):

        if user_id in self.doctors:

            doctor = self.doctors[user_id]

            if doctor.check_password(password):
                return doctor

        return None

    # ----------------------
    # Doctor availability
    # ----------------------

    def add_doctor_time(self, doctor, date, times):

        self.save_state()

        doctor.add_availability(date, *times)

    def remove_doctor_time(self, doctor, date, time):

        if not doctor.is_available(date, time):
            print("This time does not exist.")
            return

        self.save_state()
        doctor.remove_availability(date, time)

    def show_doctors(self):

        if len(self.doctors) == 0:
            print("No doctors found.")
            return

        print("\n--- Doctors ---")

        for doctor in self.doctors.values():

            print("\nDoctor ID:", doctor.user_id)
            print("Name:", doctor.name)
            print("Specialty:", doctor.specialty)

            if len(doctor.available_times) == 0:
                print("No available times.")

            else:
                print("Available times:")

                for date in doctor.available_times:
                    print(date, ":", ", ".join(doctor.available_times[date]))

    # ----------------------
    # Appointments
    # ----------------------

    def book_appointment(self, patient, doctor_id, date, time):

        if doctor_id not in self.doctors:
            print("Doctor not found.")
            return

        doctor = self.doctors[doctor_id]

        if not doctor.is_available(date, time):
            print("This time is not available.")
            return

        if patient.supported_company:
            price = 0
        else:
            price = doctor.consultation_price

        self.save_state()

        appointment = Appointment(
            self.next_appointment_id,
            patient.user_id,
            doctor.user_id,
            date,
            time,
            price
        )

        self.appointments[self.next_appointment_id] = appointment

        doctor.remove_availability(date, time)

        print("Appointment booked.")
        print("Appointment ID:", self.next_appointment_id)
        print("Price:", price)

        self.next_appointment_id += 1

    def cancel_appointment(self, patient, appointment_id):

        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return

        appointment = self.appointments[appointment_id]

        if appointment.patient_id != patient.user_id:
            print("This is not your appointment.")
            return

        if appointment.status == "Cancelled":
            print("Appointment is already cancelled.")
            return

        self.save_state()

        appointment.status = "Cancelled"

        doctor = self.doctors[appointment.doctor_id]
        doctor.add_availability(appointment.date, appointment.time)

        print("Appointment cancelled.")

    def complete_appointment(self, doctor, appointment_id):

        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return

        appointment = self.appointments[appointment_id]

        if appointment.doctor_id != doctor.user_id:
            print("This appointment is not yours.")
            return

        self.save_state()

        appointment.status = "Completed"

        print("Appointment completed.")

    def show_patient_appointments(self, patient):

        print("\n--- Appointments ---")

        found = False

        for appointment in self.appointments.values():

            if appointment.patient_id == patient.user_id:

                doctor = self.doctors[appointment.doctor_id]

                print(
                    "ID:", appointment.appointment_id,
                    "| Doctor:", doctor.name,
                    "| Date:", appointment.date,
                    "| Time:", appointment.time,
                    "| Status:", appointment.status,
                    "| Price:", appointment.price
                )

                found = True

        if not found:
            print("No appointments.")

    def show_doctor_appointments(self, doctor):

        print("\n--- Upcoming Appointments ---")

        found = False

        for appointment in self.appointments.values():

            if appointment.doctor_id == doctor.user_id:
                if appointment.status == "Upcoming":

                    patient = self.patients[appointment.patient_id]

                    print(
                        "Appointment ID:", appointment.appointment_id,
                        "| Patient:", patient.name,
                        "| Date:", appointment.date,
                        "| Time:", appointment.time
                    )

                    found = True

        if not found:
            print("No upcoming appointments.")

    # ----------------------
    # Medical items
    # ----------------------

    def add_medical_item(self, doctor, appointment_id,
                         item_type, name, price):

        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return

        appointment = self.appointments[appointment_id]

        if appointment.doctor_id != doctor.user_id:
            print("This appointment is not yours.")
            return

        patient = self.patients[appointment.patient_id]

        if item_type == "1":
            item = Radiology(
                self.next_item_id,
                name,
                price,
                appointment_id
            )

        elif item_type == "2":
            item = MedicalTest(
                self.next_item_id,
                name,
                price,
                appointment_id
            )

        elif item_type == "3":
            item = Medicine(
                self.next_item_id,
                name,
                price,
                appointment_id
            )

        else:
            print("Invalid type.")
            return

        self.save_state()

        patient.medical_record.add_item(item)

        print("Medical item added.")
        print("Item ID:", self.next_item_id)

        self.next_item_id += 1

    def edit_medical_item(self, doctor, patient, item_id):

        item = patient.medical_record.find_item(item_id)

        if item is None:
            print("Item not found.")
            return

        appointment = self.appointments[item.appointment_id]

        if appointment.doctor_id != doctor.user_id:
            print("You cannot edit this item.")
            return

        new_name = input("New name (press Enter to keep old name): ")
        new_price = input("New price (press Enter to keep old price): ")

        self.save_state()

        if new_name != "":
            item.name = new_name

        if new_price != "":
            item.price = float(new_price)

        print("Item updated.")

    def remove_medical_item(self, doctor, patient, item_id):

        item = patient.medical_record.find_item(item_id)

        if item is None:
            print("Item not found.")
            return

        appointment = self.appointments[item.appointment_id]

        if appointment.doctor_id != doctor.user_id:
            print("You cannot remove this item.")
            return

        self.save_state()

        patient.medical_record.remove_item(item_id)

        print("Item removed.")

    def show_medical_items(self, patient):

        print("\n--- Radiology / Tests / Medicines ---")

        if len(patient.medical_record.items) == 0:
            print("No medical items.")
            return

        total = 0

        for item in patient.medical_record.items:

            patient_price = item.get_patient_price(patient)

            print(
                "ID:", item.item_id,
                "| Type:", item.get_type(),
                "| Name:", item.name,
                "| Price:", patient_price
            )

            if item.item_id in patient.medical_record.results:
                print(
                    "   Result:",
                    patient.medical_record.results[item.item_id]
                )

            total += patient_price

        print("\nMedical items total:", total)

    # ----------------------
    # Results
    # ----------------------

    def add_result(self, patient, item_id, result):

        item = patient.medical_record.find_item(item_id)

        if item is None:
            print("Item not found.")
            return

        if isinstance(item, Medicine):
            print("Medicine does not have a test result.")
            return

        self.save_state()

        patient.medical_record.add_result(item_id, result)

        print("Result added.")

    # ----------------------
    # Follow ups
    # ----------------------

    def add_follow_up(self, doctor, appointment_id, date, time):

        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return

        appointment = self.appointments[appointment_id]

        if appointment.doctor_id != doctor.user_id:
            print("This appointment is not yours.")
            return

        if not doctor.is_available(date, time):
            print("This time is not available.")
            return

        self.save_state()

        follow_up = FollowUp(
            self.next_follow_up_id,
            appointment_id,
            appointment.patient_id,
            doctor.user_id,
            date,
            time
        )

        self.follow_ups[self.next_follow_up_id] = follow_up

        doctor.remove_availability(date, time)

        print("Follow-up added.")
        print("Follow-up ID:", self.next_follow_up_id)

        self.next_follow_up_id += 1

    def show_patient_follow_ups(self, patient):

        print("\n--- Follow Ups ---")

        found = False

        for follow_up in self.follow_ups.values():

            if follow_up.patient_id == patient.user_id:

                doctor = self.doctors[follow_up.doctor_id]

                print(
                    "ID:", follow_up.follow_up_id,
                    "| Doctor:", doctor.name,
                    "| Date:", follow_up.date,
                    "| Time:", follow_up.time,
                    "| Status:", follow_up.status
                )

                found = True

        if not found:
            print("No follow ups.")

    def show_doctor_follow_ups(self, doctor):

        print("\n--- Follow Ups ---")

        found = False

        for follow_up in self.follow_ups.values():

            if follow_up.doctor_id == doctor.user_id:

                patient = self.patients[follow_up.patient_id]

                print(
                    "ID:", follow_up.follow_up_id,
                    "| Patient:", patient.name,
                    "| Date:", follow_up.date,
                    "| Time:", follow_up.time
                )

                found = True

        if not found:
            print("No follow ups.")


# -------------------------------------------------
# Menus
# -------------------------------------------------

def create_patient_menu(system):

    print("\n--- Create Patient Profile ---")

    name = input("Name: ")
    phone = input("Phone: ")
    address = input("Address: ")

    company_answer = input(
        "Do you work for a supported company? (y/n): "
    ).lower()

    supported_company = company_answer == "y"

    diseases = input(
        "Chronic diseases separated by comma "
        "(press Enter if none): "
    )

    if diseases == "":
        chronic_diseases = []
    else:
        chronic_diseases = diseases.split(",")

    password = input("Password: ")

    system.create_patient(
        name,
        phone,
        address,
        supported_company,
        chronic_diseases,
        password
    )


def create_doctor_menu(system):

    print("\n--- Create Doctor Profile ---")

    name = input("Name: ")
    phone = input("Phone: ")
    address = input("Address: ")
    national_id = input("National ID: ")
    syndicate_id = input("Syndicate ID: ")
    specialty = input("Specialty: ")
    password = input("Password: ")

    system.create_doctor(
        name,
        phone,
        address,
        national_id,
        syndicate_id,
        specialty,
        password
    )


def patient_menu(system, patient):

    while True:

        print("\n--- Patient Menu ---")
        print("1. View profile")
        print("2. View doctors and available times")
        print("3. Book appointment")
        print("4. View appointments")
        print("5. View follow ups")
        print("6. View radiology, tests and medicines")
        print("7. Add radiology/test result")
        print("8. Cancel appointment")
        print("9. Change phone")
        print("10. Undo last action")
        print("0. Logout")

        choice = input("Choose: ")

        try:

            if choice == "1":
                patient.show_info()

            elif choice == "2":
                system.show_doctors()

            elif choice == "3":

                system.show_doctors()

                doctor_id = int(input("Doctor ID: "))
                date = input("Date: ")
                time = input("Time: ")

                system.book_appointment(
                    patient,
                    doctor_id,
                    date,
                    time
                )

            elif choice == "4":
                system.show_patient_appointments(patient)

            elif choice == "5":
                system.show_patient_follow_ups(patient)

            elif choice == "6":
                system.show_medical_items(patient)

            elif choice == "7":

                system.show_medical_items(patient)

                item_id = int(input("Item ID: "))
                result = input("Result: ")

                system.add_result(
                    patient,
                    item_id,
                    result
                )

            elif choice == "8":

                system.show_patient_appointments(patient)

                appointment_id = int(
                    input("Appointment ID: ")
                )

                system.cancel_appointment(
                    patient,
                    appointment_id
                )

            elif choice == "9":

                new_phone = input("New phone: ")

                system.save_state()
                patient.phone = new_phone

                print("Phone changed.")

            elif choice == "10":
                system.undo()

                # After undo, old object references may change.
                if patient.user_id in system.patients:
                    patient = system.patients[patient.user_id]

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid value.")


def appointment_menu(system, doctor, appointment):

    # Refresh objects from the system.
    appointment = system.appointments[appointment.appointment_id]
    patient = system.patients[appointment.patient_id]

    while True:

        print("\n--- Appointment ---")

        patient.show_info()

        print("\n1. Add radiology/test/medicine")
        print("2. Edit medical item")
        print("3. Remove medical item")
        print("4. View medical items")
        print("5. Add follow up")
        print("6. Complete appointment")
        print("0. Back")

        choice = input("Choose: ")

        try:

            if choice == "1":

                print("1. Diagnostic Radiology")
                print("2. Medical Test")
                print("3. Medicine")

                item_type = input("Choose type: ")
                name = input("Name: ")
                price = float(input("Price: "))

                system.add_medical_item(
                    doctor,
                    appointment.appointment_id,
                    item_type,
                    name,
                    price
                )

            elif choice == "2":

                system.show_medical_items(patient)

                item_id = int(input("Item ID: "))

                system.edit_medical_item(
                    doctor,
                    patient,
                    item_id
                )

            elif choice == "3":

                system.show_medical_items(patient)

                item_id = int(input("Item ID: "))

                system.remove_medical_item(
                    doctor,
                    patient,
                    item_id
                )

            elif choice == "4":
                system.show_medical_items(patient)

            elif choice == "5":

                print("\nDoctor available times:")

                for date in doctor.available_times:
                    print(
                        date,
                        ":",
                        ", ".join(doctor.available_times[date])
                    )

                date = input("Follow-up date: ")
                time = input("Follow-up time: ")

                system.add_follow_up(
                    doctor,
                    appointment.appointment_id,
                    date,
                    time
                )

            elif choice == "6":

                system.complete_appointment(
                    doctor,
                    appointment.appointment_id
                )

                appointment = system.appointments[
                    appointment.appointment_id
                ]

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid value.")


def follow_up_menu(system, doctor, follow_up):

    patient = system.patients[follow_up.patient_id]

    print("\n--- Follow Up ---")

    patient.show_info()

    print("\n--- Test and Radiology Results ---")

    found = False

    for item in patient.medical_record.items:

        if isinstance(item, Radiology) or isinstance(item, MedicalTest):

            print(
                "Item ID:", item.item_id,
                "|", item.get_type(),
                "|", item.name
            )

            if item.item_id in patient.medical_record.results:
                print(
                    "Result:",
                    patient.medical_record.results[item.item_id]
                )
            else:
                print("Result: Not added yet")

            found = True

    if not found:
        print("No tests or radiology.")

    while True:

        print("\n1. Add medical item")
        print("2. Edit medical item")
        print("3. Remove medical item")
        print("4. View all medical items")
        print("0. Back")

        choice = input("Choose: ")

        try:

            if choice == "1":

                print("1. Diagnostic Radiology")
                print("2. Medical Test")
                print("3. Medicine")

                item_type = input("Choose type: ")
                name = input("Name: ")
                price = float(input("Price: "))

                system.add_medical_item(
                    doctor,
                    follow_up.appointment_id,
                    item_type,
                    name,
                    price
                )

            elif choice == "2":

                system.show_medical_items(patient)

                item_id = int(input("Item ID: "))

                system.edit_medical_item(
                    doctor,
                    patient,
                    item_id
                )

            elif choice == "3":

                system.show_medical_items(patient)

                item_id = int(input("Item ID: "))

                system.remove_medical_item(
                    doctor,
                    patient,
                    item_id
                )

            elif choice == "4":
                system.show_medical_items(patient)

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid value.")


def doctor_menu(system, doctor):

    while True:

        print("\n--- Doctor Menu ---")
        print("1. View profile")
        print("2. Add available times")
        print("3. Remove available time")
        print("4. View upcoming appointments")
        print("5. Open appointment")
        print("6. View follow ups")
        print("7. Open follow up")
        print("8. Change phone")
        print("9. Undo last action")
        print("0. Logout")

        choice = input("Choose: ")

        try:

            if choice == "1":
                doctor.show_info()

            elif choice == "2":

                date = input("Date: ")

                times_input = input(
                    "Times separated by comma: "
                )

                times = times_input.split(",")

                system.add_doctor_time(
                    doctor,
                    date,
                    times
                )

                print("Available times added.")

            elif choice == "3":

                date = input("Date: ")
                time = input("Time: ")

                system.remove_doctor_time(
                    doctor,
                    date,
                    time
                )

            elif choice == "4":
                system.show_doctor_appointments(doctor)

            elif choice == "5":

                system.show_doctor_appointments(doctor)

                appointment_id = int(
                    input("Appointment ID: ")
                )

                if appointment_id not in system.appointments:
                    print("Appointment not found.")
                    continue

                appointment = system.appointments[
                    appointment_id
                ]

                if appointment.doctor_id != doctor.user_id:
                    print("This appointment is not yours.")
                    continue

                appointment_menu(
                    system,
                    doctor,
                    appointment
                )

            elif choice == "6":
                system.show_doctor_follow_ups(doctor)

            elif choice == "7":

                system.show_doctor_follow_ups(doctor)

                follow_up_id = int(
                    input("Follow-up ID: ")
                )

                if follow_up_id not in system.follow_ups:
                    print("Follow-up not found.")
                    continue

                follow_up = system.follow_ups[
                    follow_up_id
                ]

                if follow_up.doctor_id != doctor.user_id:
                    print("This follow-up is not yours.")
                    continue

                follow_up_menu(
                    system,
                    doctor,
                    follow_up
                )

            elif choice == "8":

                new_phone = input("New phone: ")

                system.save_state()
                doctor.phone = new_phone

                print("Phone changed.")

            elif choice == "9":
                system.undo()

                # Refresh doctor after undo.
                if doctor.user_id in system.doctors:
                    doctor = system.doctors[doctor.user_id]

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid value.")


def login_menu(system):

    print("\n--- Login ---")

    print("1. Patient")
    print("2. Doctor")

    role = input("Choose: ")

    try:
        user_id = int(input("ID: "))
    except ValueError:
        print("ID must be a number.")
        return

    password = input("Password: ")

    if role == "1":

        patient = system.login_patient(
            user_id,
            password
        )

        if patient is None:
            print("Wrong ID or password.")
        else:
            patient_menu(system, patient)

    elif role == "2":

        doctor = system.login_doctor(
            user_id,
            password
        )

        if doctor is None:
            print("Wrong ID or password.")
        else:
            doctor_menu(system, doctor)

    else:
        print("Invalid choice.")


def main():

    system = HospitalSystem()

    while True:

        print("\n==============================")
        print("Welcome to Future Hospital")
        print("==============================")

        print("1. Create new profile")
        print("2. Login")
        print("3. View doctors")
        print("4. Undo last action")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":

            print("\n1. Patient")
            print("2. Doctor")

            role = input("Choose: ")

            if role == "1":
                create_patient_menu(system)

            elif role == "2":
                create_doctor_menu(system)

            else:
                print("Invalid choice.")

        elif choice == "2":
            login_menu(system)

        elif choice == "3":
            system.show_doctors()

        elif choice == "4":
            system.undo()

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
