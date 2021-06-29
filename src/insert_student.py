from dao.student_dao import StudentDAO

forename = input('enter first name: ')
surname = input('enter last name: ')
year_group = input('enter year group: ')
email = input('enter only the first part of the email: ')
student_details = (forename, surname, email, year_group)

print(StudentDAO.insert_student(student_details))
