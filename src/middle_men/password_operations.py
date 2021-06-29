import bcrypt as bc


class PasswordOperations:

    @staticmethod
    def get_hashed_password_po(password):
        hashed_password = bc.hashpw(password.encode('utf8'), bc.gensalt())
        return hashed_password

    @staticmethod
    def compare_password(input_password, hashed_password):
        if bc.hashpw(input_password.encode('utf8'), hashed_password) == hashed_password:
            # in the above statement, the hashed_password itself is passed as an argument to a parameter
            # accepts salt. this is because the library would extract the salt from the hashed_password
            # and add the same salt to the input password and then hash it, so if the passwords are same,
            # the salted hashed values will also be the same
            return True
        else:
            return False
