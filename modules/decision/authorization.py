from modules.behavior.notification import NotificationComponent
from modules.decision.context import ContextComponent
from modules.decision.activity import ActivityComponent
from modules.decision.ontology import OntologyComponent
from modules.behavior.configuration import ConfigurationComponent
from models_zash import Request
from datetime import datetime, timedelta


class AuthorizationComponent:
    def __init__(self, configuration_component: ConfigurationComponent, ontology_component: OntologyComponent,
                 context_component: ContextComponent, activity_component: ActivityComponent,
                 notification_component: NotificationComponent):
        self.configuration_component = configuration_component
        self.ontology_component = ontology_component
        self.context_component = context_component
        self.activity_component = activity_component
        self.notification_component = notification_component
        self.limit_date = None

    # checks for:
    #   - Ontology Component
    #   - Context Component
    #   - Activity Component
    # in order, and blocks user if failed enough within interval
    # sends notifications to users about blockage
    def on_request(self, req: Request, current_state: list, last_state: list, current_date: datetime):
        print("Authorization Component")
        print("Processing Request: {}".format(str(req)))
        self.check_markov(current_date)
        self.check_users(current_date)
        if req.user.blocked:
            print("USER IS BLOCKED - Request is NOT authorized!")
            return False
        if not self.ontology_component.verify_ontology(req) or \
                not self.context_component.verify_context(req) or \
                not self.activity_component.verify_activity(current_state, last_state):
            req.user.rejected.append(current_date)
            print("User have now {} rejected requests!".format(
                len(req.user.rejected)))
            if len(req.user.rejected) > self.configuration_component.block_threshold:
                req.user.blocked = True
                print("User {} is blocked!".format(req.user))
                for user in self.configuration_component.users:
                    self.notification_component.send_message(
                        user, "User {} is blocked!".format(req.user))
            print("Request is NOT authorized!")
            return False
        print("Request is authorized!")
        return True

    # check if markov build time expired
    def check_markov(self, current_date: datetime):
        if self.limit_date is None:
            self.limit_date = current_date + \
                timedelta(
                    days=self.configuration_component.markov_build_interval)
        elif self.activity_component.is_markov_building and current_date > self.limit_date:
            self.activity_component.is_markov_building = False
            print("Markov Chain stopped building transition matrix at {}".format(
                current_date))
    
    # clean rejects occurred out of interval
    def check_users(self, current_date: datetime):
        for user in self.configuration_component.users:
            user.rejected = [rej_date for rej_date in user.rejected if current_date -
                             rej_date < timedelta(hours=self.configuration_component.block_interval)]
