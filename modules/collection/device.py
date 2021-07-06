from datetime import datetime, timedelta
from modules.audit.audit import AuditComponent, AuditEvent
from models_zash import Request
from modules.collection.data import DataComponent
from modules.decision.authorization import AuthorizationComponent


PROOF_EXPIRATION = 10  # minutes


class DeviceComponent:
    def __init__(self, configuration_component: list, authorization_component: AuthorizationComponent, data_component: DataComponent, audit_component: AuditComponent):
        self.configuration_component = configuration_component
        self.authorization_component = authorization_component
        self.data_component = data_component
        self.audit_component = audit_component
        self.proofs = []

    def explicit_authentication(self, req: Request, current_date: datetime):
        proof = next((proof for proof in self.proofs if proof['user'] ==
                      req.user.id and proof['access_way'] == req.context.access_way), None)
        if not proof:
            print("Please provide proof of identity:")
            # proof = int(input())
            proof = req.user.id
            if proof != req.user.id:
                self.audit_component.invalid_proofs.append(
                    AuditEvent(current_date, req))
                print("Proof does not match")
                return False
            else:
                self.audit_component.valid_proofs.append(
                    AuditEvent(current_date, req))
                self.proofs.append(
                    {"user": req.user.id, "access_way": req.context.access_way, "current_date": current_date})
        print("Proof matches")
        return True

    def clear_proofs(self, current_date: datetime):
        self.proofs = [proof for proof in self.proofs if current_date -
                       proof['current_date'] < timedelta(minutes=PROOF_EXPIRATION)]

    def listen_request(self, req: Request, current_date: datetime):
        self.clear_proofs(current_date)
        self.data_component.update_current_state(req)
        result = True
        if req.device.active:
            print("Active {} request changing state from {} to {}".format(
                req.device, self.data_component.last_state[req.device.id - 1], self.data_component.current_state[req.device.id - 1]))
            self.audit_component.req_number += 1
            result = self.authorization_component.authorize_request(
                req, current_date, self.explicit_authentication)
        else:
            print("Passive {} changed state from {} to {}".format(
                req.device, self.data_component.last_state[req.device.id - 1], self.data_component.current_state[req.device.id - 1]))
        self.data_component.update_last_state()
        return result
