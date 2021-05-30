from models_zash import User


class NotificationComponent:
    def send_message(self, user: User, message: str):
        print("User {} received message: '{}'".format(user, message))