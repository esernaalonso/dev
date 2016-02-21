"""Summary"""
#######################################
# imports

import esa.common.python.tool.inside_anim.campus.db.db as db

reload(db)

#######################################
# functionality


class Credentials(object):
    def __init__(self, user=None, password=None):
        self.user = user
        self.password = password
        self.validated = False
        self.connection_message = ""

        if self.user and self.password:
            self.validate(self.user, self.password)

    def validate(self, user, password):
        self.connection_message = ""
        self.validated = db.check_connection()

        if self.validated:
            self.validated = db.check_user_password(user, password)

            if not self.validated:
                self.connection_message = "Unable to log in the system. Check the user and/or password."
        else:
            self.connection_message = "Unable to connect with the database, check your internet connection and if the problem persists, contact the technical service."

        return self.validated

    def is_validated(self):
        return self.validated

    def get_connection_message(self):
        return self.connection_message



#######################################
# execution

if __name__ == "__main__":
    pass
