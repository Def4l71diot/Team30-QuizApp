import hashlib, uuid

from quiz_app_framework.data import UserDatabase


class ConfigManager:

    def __init__(self, user_database=UserDatabase()):
        self._user_database = user_database
        self.is_first_launch = self._user_database.get_number_of_records() == 0
        self.is_admin_logged_in = False

    def login_admin(self, password):
        if self.is_first_launch:
            raise Exception("Admin account not found!")

        if self.is_admin_logged_in:
            raise Exception("Admin already logged in!")

        [admin] = self._user_database.get_all()
        password_hash = hashlib.sha512((password + admin.salt).encode('utf-8')).hexdigest()

        if password_hash == admin.password_hash:
            self.is_admin_logged_in = True
        else:
            self.is_admin_logged_in = False

        return self.is_admin_logged_in

    def register_admin(self, password):
        if not self.is_first_launch:
            Exception("Admin account already created!")

        # reference:
        # https://stackoverflow.com/a/9595108 Mar 7 '12 at 2:44
        # Generate password hash with salt
        salt = uuid.uuid4().hex
        password_hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
        # end reference

        admin = self._user_database.add(password_hash=password_hash, salt=salt)

        if admin is None:
            return False

        self.is_first_launch = False

        return True

    def logout_admin(self):
        self.is_admin_logged_in = False
