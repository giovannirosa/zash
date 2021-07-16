import csv
from modules.audit.audit import AuditComponent
from modules.collection.data import DataComponent
from modules.collection.device import DeviceComponent
from modules.decision.authorization import AuthorizationComponent
from modules.behavior.notification import NotificationComponent
from modules.decision.activity import ActivityComponent
from modules.decision.context import ContextComponent
from modules.decision.ontology import OntologyComponent
from modules.behavior.configuration import ConfigurationComponent
from datetime import datetime
from enums_zash import *
from models_zash import *
import sys
import os

NUMBER_OF_DEVICES = 29
ACTIVITY_COL = 29
DATE_COL = 30

log_id = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
dir = "logs/sim_{}".format(log_id)
os.mkdir(dir)


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(os.path.join(dir, "sim_{}.txt".format(log_id)), "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


sys.stdout = Logger()

users = [User(1, UserLevel.ADMIN, Age.ADULT), User(2, UserLevel.ADULT, Age.ADULT), User(
    3, UserLevel.CHILD, Age.TEEN), User(4, UserLevel.CHILD, Age.KID), User(5, UserLevel.VISITOR, Age.ADULT)]
devices = [Device(1, "Wardrobe", DeviceClass.NONCRITICAL, Room.BEDROOM, True),  # wardrobe
           Device(2, "TV", DeviceClass.NONCRITICAL,
                  Room.LIVINGROOM, True),  # tv
           Device(3, "Oven", DeviceClass.CRITICAL, Room.KITCHEN, True),  # oven
           Device(4, "Office Light", DeviceClass.NONCRITICAL,
                  Room.OFFICE, True),  # officeLight
           Device(5, "Office Door Lock", DeviceClass.CRITICAL,
                  Room.OFFICE, True),  # officeDoorLock
           Device(6, "Office Door", DeviceClass.NONCRITICAL,
                  Room.OFFICE, True),  # officeDoor
           Device(7, "Office Carpet", DeviceClass.NONCRITICAL,
                  Room.OFFICE, False),  # officeCarp
           Device(8, "Office", DeviceClass.NONCRITICAL,
                  Room.OFFICE, False),  # office
           Device(9, "Main Door Lock", DeviceClass.CRITICAL,
                  Room.HOUSE, True),  # mainDoorLock
           Device(10, "Main Door", DeviceClass.NONCRITICAL,
                  Room.HOUSE, True),  # mainDoor
           Device(11, "Living Light", DeviceClass.NONCRITICAL,
                  Room.LIVINGROOM, True),  # livingLight
           Device(12, "Living Carpet", DeviceClass.NONCRITICAL,
                  Room.LIVINGROOM, False),  # livingCarp
           Device(13, "Kitchen Light", DeviceClass.NONCRITICAL,
                  Room.KITCHEN, True),  # kitchenLight
           Device(14, "Kitchen Door Lock", DeviceClass.CRITICAL,
                  Room.KITCHEN, True),  # kitchenDoorLock
           Device(15, "Kitchen Door", DeviceClass.NONCRITICAL,
                  Room.KITCHEN, True),  # kitchenDoor
           Device(16, "Kitchen Carpet", DeviceClass.NONCRITICAL,
                  Room.KITCHEN, False),  # kitchenCarp
           Device(17, "Hallway Light", DeviceClass.NONCRITICAL,
                  Room.HOUSE, True),  # hallwayLight
           Device(18, "Fridge", DeviceClass.CRITICAL,
                  Room.KITCHEN, True),  # fridge
           Device(19, "Couch", DeviceClass.NONCRITICAL,
                  Room.LIVINGROOM, False),  # couch
           Device(20, "Bedroom Light", DeviceClass.NONCRITICAL,
                  Room.BEDROOM, True),  # bedroomLight
           Device(21, "Bedroom Door Lock", DeviceClass.CRITICAL,
                  Room.BEDROOM, True),  # bedroomDoorLock
           Device(22, "Bedroom Door", DeviceClass.NONCRITICAL,
                  Room.BEDROOM, True),  # bedroomDoor
           Device(23, "Bedroom Carpet", DeviceClass.NONCRITICAL,
                  Room.BEDROOM, False),  # bedroomCarp
           Device(24, "Bed Table Lamp", DeviceClass.NONCRITICAL,
                  Room.BEDROOM, True),  # bedTableLamp
           Device(25, "Bed", DeviceClass.NONCRITICAL,
                  Room.BEDROOM, False),  # bed
           Device(26, "Bathroom Light", DeviceClass.NONCRITICAL,
                  Room.BATHROOM, True),  # bathroomLight
           Device(27, "Bathroom Door Lock", DeviceClass.CRITICAL, Room.BATHROOM,
                  True),  # bathroomDoorLock
           Device(28, "Bathroom Door", DeviceClass.NONCRITICAL,
                  Room.BATHROOM, True),  # bathroomDoor
           Device(29, "Bathroom Carpet", DeviceClass.NONCRITICAL, Room.BATHROOM, False)]  # bathroomCarp


visitor_critical = Ontology(UserLevel.VISITOR, DeviceClass.CRITICAL, [])
child_critical = Ontology(UserLevel.CHILD, DeviceClass.CRITICAL,
                          visitor_critical.capabilities + [Action.VIEW])
adult_critical = Ontology(UserLevel.ADULT, DeviceClass.CRITICAL,
                          child_critical.capabilities + [Action.CONTROL])
admin_critical = Ontology(UserLevel.ADMIN, DeviceClass.CRITICAL,
                          adult_critical.capabilities + [Action.MANAGE])

visitor_noncritical = Ontology(UserLevel.VISITOR, DeviceClass.NONCRITICAL, [
    Action.VIEW, Action.CONTROL])
child_noncritical = Ontology(
    UserLevel.CHILD, DeviceClass.NONCRITICAL, visitor_noncritical.capabilities + [])
adult_noncritical = Ontology(UserLevel.ADULT, DeviceClass.NONCRITICAL,
                             child_noncritical.capabilities + [Action.MANAGE])
admin_noncritical = Ontology(
    UserLevel.ADMIN, DeviceClass.NONCRITICAL, adult_noncritical.capabilities)

ontologies = [visitor_critical, child_critical, adult_critical,
              admin_critical, visitor_noncritical, child_noncritical, adult_noncritical, admin_noncritical]

# Audit Module
audit_module = AuditComponent()

# Behavior Module
configuration_component = ConfigurationComponent(
    3, 24, 32, devices, users, ontologies)
notification_component = NotificationComponent(configuration_component)

# Collection Module
data_component = DataComponent()

# Decision Module
ontology_component = OntologyComponent(configuration_component, audit_module)
context_component = ContextComponent(configuration_component, audit_module)
activity_component = ActivityComponent(
    data_component, configuration_component, audit_module)
authorization_component = AuthorizationComponent(
    configuration_component, ontology_component, context_component, activity_component, notification_component, audit_module)

# Collection Module
device_component = DeviceComponent(
    configuration_component, authorization_component, data_component, audit_module)


tests = [
    # {
    #     "req": 1480,  # activity
    #     "user": users[1],
    #     "context": Context(AccessWay.PERSONAL, Localization.EXTERNAL, Group.ALONE),
    #     "action": Action.CONTROL
    # },
    # {
    #     "req": 2518,  # context
    #     "user": users[0],
    #     "context": Context(AccessWay.REQUESTED, Localization.EXTERNAL, Group.ALONE),
    #     "action": Action.MANAGE
    # },
    # {
    #     "req": 9,  # ontology
    #     "user": users[3],
    #     "context": Context(AccessWay.PERSONAL, Localization.INTERNAL, Group.ALONE),
    #     "action": Action.CONTROL
    # },
]

sim_user = users[2]
sim_context = Context(
    AccessWay.PERSONAL, Localization.INTERNAL, Group.ALONE)
sim_action = Action.CONTROL

id_req = 0
# 174,809 lines of records, 2 months, 60 days, 1 line per second
with open('data/d6_2m_0tm.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    for row in spamreader:
        current_date = datetime.strptime(
            row[DATE_COL], '%Y-%m-%d %H:%M:%S')

        # if current_date < datetime.strptime('2016-03-05 11:09:24', '%Y-%m-%d %H:%M:%S'):
        #     current_state = list(
        #         map(int, row[0:17] + row[18:NUMBER_OF_DEVICES]))
        # else:
        current_state = list(map(int, row[:NUMBER_OF_DEVICES]))
        # if len(data_component.last_state) == 28:
        #     data_component.last_state[17:17] = [0]

        if current_state == data_component.last_state:
            continue

        act = Activity(ActivityEnum[row[ACTIVITY_COL].upper()])

        if data_component.last_state is not None:
            changes = [(i, e1, e2) for i, (e1, e2) in enumerate(
                zip(data_component.last_state, current_state)) if e1 != e2]
            for change in changes:
                print(current_date, act)
                id_req += 1
                test = next(
                    (test for test in tests if test["req"] == id_req), None)
                req = Request(
                    id_req, devices[change[0]], sim_user, sim_context, sim_action)
                if test:
                    req.user = test["user"]
                    req.context = test["context"]
                    req.action = test["action"]
                device_component.listen_request(req, current_date)
                print()
        else:
            data_component.last_state = current_state

admin_users = len(
    list(filter(lambda user: user.user_level == UserLevel.ADMIN, users)))
critical_devices = len(list(
    filter(lambda device: device.device_class == DeviceClass.CRITICAL, devices)))


print("\nSimulation user:")
print(sim_user)
print()

print("\nSimulation context:")
print(sim_context)

print("\nSimulation action:")
print(sim_action)


def print_values(enum: Enum):
    for en in enum:
        print("{} - {}".format(en.name, en.value[1]))


print("\nSimulation configuration:")
print("User Level")
print_values(UserLevel)
print()

print("Action")
print_values(Action)
print()

print("Device Class")
print_values(DeviceClass)
print()


print("\nSimulation context factors:")

print("Time")
print_values(TimeClass)
print()

print("Localization")
print_values(Localization)
print()

print("Age")
print_values(Age)
print()

print("Group")
print_values(Group)
print()

print("Access Way")
print_values(AccessWay)
print()


print("\nSimulation metrics:")

# print("PR = {}".format(admin_users * critical_devices))

# print("DE = {}".format(29 - 28))

# print("RI = {}".format(len(UserLevel) * len(DeviceClass)))

# print("SD = {}".format(len(Action) * len(DeviceClass)))

with open(os.path.join(dir, "blocks_{}.txt".format(log_id)), "w") as writer:
    writer.writelines([str(event) for event in audit_module.blocks])

with open(os.path.join(dir, "ontology_fail_{}.txt".format(log_id)), "w") as writer:
    writer.writelines([str(event) for event in audit_module.ontology_fail])

with open(os.path.join(dir, "context_fail_{}.txt".format(log_id)), "w") as writer:
    writer.writelines([str(event) for event in audit_module.context_fail])

with open(os.path.join(dir, "activity_fail_{}.txt".format(log_id)), "w") as writer:
    writer.writelines([str(event) for event in audit_module.activity_fail])

with open(os.path.join(dir, "valid_proofs_{}.txt".format(log_id)), "w") as writer:
    writer.writelines([str(event) for event in audit_module.valid_proofs])

with open(os.path.join(dir, "invalid_proofs_{}.txt".format(log_id)), "w") as writer:
    writer.writelines([str(event) for event in audit_module.invalid_proofs])

req_number = audit_module.req_number


def percentage(number, total):
    return "0.0%" if total == 0 else "{}%".format(str(round(number / total * 100, 2)))


print("REQUESTS NUMBER = {}".format(req_number))

req_granted = audit_module.req_granted
print("REQUESTS GRANTED = {} ({})".format(
    req_granted, percentage(req_granted, req_number)))

req_refused = audit_module.req_refused
print("REQUESTS REFUSED = {} ({})".format(
    req_refused, percentage(req_refused, req_number)))

ontology_fail = len(audit_module.ontology_fail)
print("ONTOLOGY FAILS = {} ({})".format(
    ontology_fail, percentage(ontology_fail, req_number)))

context_fail = len(audit_module.context_fail)
print("CONTEXT FAILS = {} ({})".format(
    context_fail, percentage(context_fail, req_number)))

activity_fail = len(audit_module.activity_fail)
print("ACTIVITY FAILS = {} ({})".format(
    activity_fail, percentage(activity_fail, req_number)))

valid_proofs = len(audit_module.valid_proofs)
invalid_proofs = len(audit_module.invalid_proofs)
print("VALID PROOFS = {} ({})".format(valid_proofs, percentage(
    valid_proofs, valid_proofs + invalid_proofs)))
print("INVALID PROOFS = {} ({})".format(invalid_proofs, percentage(
    invalid_proofs, valid_proofs + invalid_proofs)))

print("BLOCKS = {}".format(len(audit_module.blocks)))