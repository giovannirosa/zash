from markov_zash import MarkovChain
from enums_zash import *
from datetime import datetime


class Activity:
    def __init__(self, activity):
        self.activity = activity

    def __repr__(self):
        return str(self.activity)

    def __str__(self):
        return str(self.activity)


class Context:
    def __init__(self, access_way: AccessWay, localization: Localization, time: Time, age: Age, group: Group):
        self.access_way = access_way
        self.localization = localization
        self.time = time
        self.age = age
        self.group = group

    def __repr__(self):
        return "Context[{},{},{},{},{}]".format(str(self.access_way), str(self.localization), str(self.time), str(self.age), str(self.group))

    def __str__(self):
        return "Context[{},{},{},{},{}]".format(str(self.access_way), str(self.localization), str(self.time), str(self.age), str(self.group))

    def trust(self):
        return self.access_way.value[1] + self.localization.value[1] + self.time.value[1] + self.age.value[1] + self.group.value[1]


class Ontology:
    def __init__(self, user_level: UserLevel, device_class: DeviceClass, capabilities: list):
        self.user_level = user_level
        self.device_class = device_class
        self.capabilities = capabilities

    def __repr__(self):
        return "Ontology[{},{},{}]".format(str(self.user_level), str(self.device_class), str(self.capabilities))

    def __str__(self):
        return "Ontology[{},{},{}]".format(str(self.user_level), str(self.device_class), str(self.capabilities))


class User:
    def __init__(self, id: int, user_level: UserLevel):
        self.id = id
        self.user_level = user_level
        self.rejected = []
        self.start_interval = None
        self.blocked = False

    def __repr__(self):
        return "User[{},{}]".format(str(self.id), str(self.user_level))

    def __str__(self):
        return "User[{},{}]".format(str(self.id), str(self.user_level))


class Device:
    def __init__(self, id: int, device_class: DeviceClass, room: Room, active: bool):
        self.id = id
        self.device_class = device_class
        self.room = room
        self.active = active

    def __repr__(self):
        return "Device[{},{},{}]".format(str(self.id), str(self.device_class), str(self.room))

    def __str__(self):
        return "Device[{},{},{}]".format(str(self.id), str(self.device_class), str(self.room))


class Request:
    def __init__(self, id: int, device: Device, user: User, context: Context, action: Action):
        self.id = id
        self.device = device
        self.user = user
        self.context = context
        self.action = action

    def __repr__(self):
        return "Request[{},{},{},{},{}]".format(str(self.id), str(self.device), str(self.user), str(self.context), str(self.action))

    def __str__(self):
        return "Request[{},{},{},{},{}]".format(str(self.id), str(self.device), str(self.user), str(self.context), str(self.action))


class ConfigurationComponent:
    def __init__(self, block_threshold: int, block_interval: int, markov_build_interval: int, devices: list, users: list, ontologies: list):
        self.block_threshold = block_threshold
        self.block_interval = block_interval
        self.markov_build_interval = markov_build_interval
        self.devices = devices
        self.users = users
        self.ontologies = ontologies


class OntologyComponent:
    def __init__(self, configuration_component: ConfigurationComponent):
        self.configuration_component = configuration_component

    # common ontologies like:
    #   - critical devices:
    #       - visitor cannot even visualize
    #       - kids can only visualize
    #       - adults can only visualize and control
    #       - admins can visualize, control and manage
    #   - non-critical devices:
    #       - visitor and kids can visualize and control
    #       - adults and admins can visualize, control and manage
    def verify_ontology(self, req: Request):
        print("Ontology Component")
        print("Verify User Level {} with the Action {} on the device class {}".format(
            req.user.user_level, req.action, req.device.device_class))
        compatible = True
        print(self.configuration_component.ontologies)
        capabilities = next((ontology.capabilities for ontology in self.configuration_component.ontologies if ontology.user_level ==
                                   req.user.user_level and ontology.device_class == req.device.device_class), [])
        print(capabilities)
        if req.action in capabilities:
            compatible = True
        else:
            compatible = False
        str_result = 'compatible'
        if not compatible:
            str_result = 'incompatible'
        print("User level {} is {} with the Action {} on the device class {}".format(
            req.user.user_level, str_result, req.action, req.device.device_class))
        return compatible


class ContextComponent:
    # static trust calculation based on expected
    # for [DeviceClass x Action] and [UserLevel x Action]
    # from [AccessWay, Localization, Time, Age, Group]
    def verify_context(self, req: Request):
        print("Context Component")
        print("Verify context {}".format(req.context))
        expected_device = req.device.device_class.value[1] + \
            req.action.value[1]
        expected_user = req.user.user_level.value[1] + req.action.value[1]
        expected = max(expected_device, expected_user)
        print("Trust level is {} and expected is {}".format(
            req.context.trust(), expected))
        if req.context.trust() < expected:
            print("Trust level is BELOW expected!")
            return False
        print("Trust level is ABOVE expected!")
        return True


class ActivityComponent:
    def __init__(self):
        self.markov_chain = MarkovChain()
        self.is_markov_building = True

    # check next state probability using a Markov Chain
    # updates transition matrix with successful requests
    def verify_activity(self, current_state, last_state):
        print("Activity Component")
        print("Verify activities")
        print("From: {}".format(last_state))
        print("To: {}".format(current_state))
        if self.is_markov_building:
            self.markov_chain.build_transition(current_state, last_state)
            return True
        else:
            prob = self.markov_chain.get_probability(current_state, last_state)
            if prob > 0:
                self.markov_chain.build_transition(current_state, last_state)
                print("Activity is valid!")
                return True
            else:
                print("Activity is NOT valid!")
                return False


class NotificationComponent:
    def send_message(self, user: User, message: str):
        print("User {} received message: '{}'".format(user, message))


class AuthorizationComponent:
    def __init__(self, configuration_component: ConfigurationComponent, ontology_component: OntologyComponent,
                 context_component: ContextComponent, activity_component: ActivityComponent,
                 notification_component: NotificationComponent):
        self.configuration_component = configuration_component
        self.ontology_component = ontology_component
        self.context_component = context_component
        self.activity_component = activity_component
        self.notification_component = notification_component

    # checks for:
    #   - Ontology Component
    #   - Context Component
    #   - Activity Component
    # in order, and blocks user if failed enough within interval
    # sends notifications to users about blockage
    def on_request(self, req: Request, current_state: list, last_state: list, current_date: datetime):
        print("Authorization Component")
        print("Processing Request: {}".format(str(req)))
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
