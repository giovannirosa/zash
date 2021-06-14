from datetime import datetime, timedelta
from models_zash import Request
from modules.collection.data import DataComponent
from modules.decision.authorization import AuthorizationComponent


class DeviceComponent:
    def __init__(self, configuration_component: list, authorization_component: AuthorizationComponent, data_component: DataComponent):
        self.configuration_component = configuration_component
        self.authorization_component = authorization_component
        self.data_component = data_component
        self.proofs = []

    def explicit_authentication(self, req: Request, current_date: datetime):
        proof = next((proof for proof in self.proofs if proof['user'] ==
                      req.user.id and proof['access_way'] == req.context.access_way), None)
        if not proof:
            print("Please provide proof of identity:")
            # proof = int(input())
            proof = 1
            if proof != req.user.id:
                print("Proof does not match")
                return False
            else:
                self.proofs.append(
                    {"user": req.user.id, "access_way": req.context.access_way, "current_date": current_date})
        print("Proof matches")
        return True

    def clear_proofs(self, current_date: datetime):
        self.proofs = [proof for proof in self.proofs if current_date -
                       proof['current_date'] < timedelta(minutes=10)]

    def listen_request(self, req: Request, current_date: datetime):
        self.clear_proofs(current_date)
        self.data_component.update_current_state(req)
        result = self.authorization_component.authorize_request(
            req, current_date, self.explicit_authentication)
        self.data_component.update_last_state()
        return result
