from modules.behavior.configuration import ConfigurationComponent
from models_zash import User


class NotificationComponent:
    def __init__(self, configuration_component: ConfigurationComponent):
        self.configuration_component = configuration_component

    def alert_users(self, blocked_user: User):
        for user in self.configuration_component.users:
            print("{} received message: '{}'".format(user, "{} is blocked!".format(blocked_user)))
