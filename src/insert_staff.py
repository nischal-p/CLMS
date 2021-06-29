from dao.staff_dao import StaffDAO
from middle_men.password_operations import PasswordOperations

forename = input('enter first name: ')
surname = input('enter last name: ')
email = input('enter only the first part of the email: ')
hashed_password = PasswordOperations.get_hash(input('enter password: '))
staff_details = (forename, surname, email, hashed_password)

print(StaffDAO.insert_staff(staff_details))