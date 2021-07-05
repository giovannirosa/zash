from modules.audit.audit import AuditComponent, AuditEvent
from modules.behavior.notification import NotificationComponent
from modules.decision.context import ContextComponent
from modules.decision.activity import ActivityComponent
from modules.decision.ontology import OntologyComponent
from modules.behavior.configuration import ConfigurationComponent
from models_zash import Request
from datetime import datetime, timedelta
from typing import Callable


class AuthorizationComponent:
    def __init__(self, configuration_component: ConfigurationComponent, ontology_component: OntologyComponent,
                 context_component: ContextComponent, activity_component: ActivityComponent,
                 notification_component: NotificationComponent, audit_component: AuditComponent):
        self.configuration_component = configuration_component
        self.ontology_component = ontology_component
        self.context_component = context_component
        self.activity_component = activity_component
        self.notification_component = notification_component
        self.audit_component = audit_component

    # checks for:
    #   - Ontology Component
    #   - Context Component
    #   - Activity Component
    # in order, and blocks user if failed enough within interval
    # sends notifications to users about blockage
    def authorize_request(self, req: Request, current_date: datetime, explicit_authentication: Callable):
        print("Authorization Component")
        print("Processing Request: {}".format(str(req)))
        self.check_users(current_date)
        if req.user.blocked:
            print("USER IS BLOCKED - Request is NOT authorized!")
            return False
        if not self.ontology_component.verify_ontology(req, current_date) or \
                not self.context_component.verify_context(req, current_date, explicit_authentication) or \
                not self.activity_component.verify_activity(req, current_date, explicit_authentication):
            req.user.rejected.append(current_date)
            print("User have now {} rejected requests!".format(
                len(req.user.rejected)))
            if len(req.user.rejected) > self.configuration_component.block_threshold:
                self.audit_component.blocks.append(
                    AuditEvent(current_date, req))
                req.user.blocked = True
                print("{} is blocked!".format(req.user))
                self.notification_component.alert_users(req.user)
            print("Request is NOT authorized!")
            return False
        print("Request is authorized!")
        return True

    # clean rejects occurred out of interval
    def check_users(self, current_date: datetime):
        for user in self.configuration_component.users:
            user.rejected = [rej_date for rej_date in user.rejected if current_date -
                             rej_date < timedelta(hours=self.configuration_component.block_interval)]
