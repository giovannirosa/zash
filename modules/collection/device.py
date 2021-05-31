from datetime import datetime
from modules.collection.data import DataComponent
from modules.decision.authorization import AuthorizationComponent
from models_zash import Request


class DeviceComponent:
    def __init__(self, configuration_component: list, authorization_component: AuthorizationComponent, data_component: DataComponent):
        self.configuration_component = configuration_component
        self.authorization_component = authorization_component
        self.data_component = data_component

    def listen_request(self, req: Request, current_date: datetime):
        self.data_component.update_current_state(req)
        result = self.authorization_component.authorize_request(req, current_date)
        self.data_component.update_last_state()
        return result
