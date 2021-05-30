import csv
from modules.decision.authorization import AuthorizationComponent
from modules.behavior.notification import NotificationComponent
from modules.decision.activity import ActivityComponent
from modules.decision.context import ContextComponent
from modules.decision.ontology import OntologyComponent
from modules.behavior.configuration import ConfigurationComponent
import queue
from datetime import datetime, timedelta
from enums_zash import *
from models_zash import *


WINDOW_SIZE = 5
NUMBER_OF_DEVICES = 29
ACTIVITY_COL = 29
DATE_COL = 30

users = [User(1, UserLevel.ADMIN), User(2, UserLevel.ADULT), User(
    3, UserLevel.CHILD), User(4, UserLevel.CHILD), User(5, UserLevel.VISITOR)]
devices = [Device(1, DeviceClass.NONCRITICAL, Room.BEDROOM, True),  # wardrobe
           Device(2, DeviceClass.NONCRITICAL, Room.LIVINGROOM, True),  # tv
           Device(3, DeviceClass.CRITICAL, Room.KITCHEN, True),  # oven
           Device(4, DeviceClass.NONCRITICAL,
                  Room.OFFICE, True),  # officeLight
           Device(5, DeviceClass.CRITICAL, Room.OFFICE, True),  # officeDoorLock
           Device(6, DeviceClass.NONCRITICAL, Room.OFFICE, True),  # officeDoor
           Device(7, DeviceClass.NONCRITICAL,
                  Room.OFFICE, False),  # officeCarp
           Device(8, DeviceClass.NONCRITICAL, Room.OFFICE, False),  # office
           Device(9, DeviceClass.CRITICAL, Room.HOUSE, True),  # mainDoorLock
           Device(10, DeviceClass.NONCRITICAL, Room.HOUSE, True),  # mainDoor
           Device(11, DeviceClass.NONCRITICAL,
                  Room.LIVINGROOM, True),  # livingLight
           Device(12, DeviceClass.NONCRITICAL,
                  Room.LIVINGROOM, False),  # livingCarp
           Device(13, DeviceClass.NONCRITICAL,
                  Room.KITCHEN, True),  # kitchenLight
           Device(14, DeviceClass.CRITICAL,
                  Room.KITCHEN, True),  # kitchenDoorLock
           Device(15, DeviceClass.NONCRITICAL,
                  Room.KITCHEN, True),  # kitchenDoor
           Device(16, DeviceClass.NONCRITICAL,
                  Room.KITCHEN, False),  # kitchenCarp
           Device(17, DeviceClass.NONCRITICAL,
                  Room.HOUSE, True),  # hallwayLight
           Device(18, DeviceClass.CRITICAL, Room.KITCHEN, True),  # fridge
           Device(19, DeviceClass.NONCRITICAL,
                  Room.LIVINGROOM, False),  # couch
           Device(20, DeviceClass.NONCRITICAL,
                  Room.BEDROOM, True),  # bedroomLight
           Device(21, DeviceClass.CRITICAL,
                  Room.BEDROOM, True),  # bedroomDoorLock
           Device(22, DeviceClass.NONCRITICAL,
                  Room.BEDROOM, True),  # bedroomDoor
           Device(23, DeviceClass.NONCRITICAL,
                  Room.BEDROOM, False),  # bedroomCarp
           Device(24, DeviceClass.NONCRITICAL,
                  Room.BEDROOM, True),  # bedTableLamp
           Device(25, DeviceClass.NONCRITICAL, Room.BEDROOM, False),  # bed
           Device(26, DeviceClass.NONCRITICAL,
                  Room.BATHROOM, True),  # bathroomLight
           Device(27, DeviceClass.CRITICAL, Room.BATHROOM,
                  True),  # bathroomDoorLock
           Device(28, DeviceClass.NONCRITICAL,
                  Room.BATHROOM, True),  # bathroomDoor
           Device(29, DeviceClass.NONCRITICAL, Room.BATHROOM, False)]  # bathroomCarp


# act_window = queue.Queue(WINDOW_SIZE)
# requests = [{"time": "2016-03-03 18:30:31", "req": Request(1, devices[8], users[4], Context(
#     AccessWay.REQUESTED, Localization.INTERNAL, Time.UNCOMMOM, Age.KID, Group.ALONE), Action.CONTROL)}]

visitor_critical = Ontology(UserLevel.VISITOR, DeviceClass.CRITICAL, [])
child_critical = Ontology(UserLevel.CHILD, DeviceClass.CRITICAL,
                          visitor_critical.capabilities + [Action.VIEW])
adult_critical = Ontology(UserLevel.ADULT, DeviceClass.CRITICAL,
                          child_critical.capabilities + [Action.CONTROL])
admin_critical = Ontology(UserLevel.ADMIN, DeviceClass.CRITICAL,
                          adult_critical.capabilities + [Action.MANAGE])

visitor_noncritical = Ontology(UserLevel.VISITOR, DeviceClass.CRITICAL, [
                               Action.VIEW, Action.CONTROL])
child_noncritical = Ontology(
    UserLevel.CHILD, DeviceClass.NONCRITICAL, visitor_noncritical.capabilities + [])
adult_noncritical = Ontology(UserLevel.ADULT, DeviceClass.NONCRITICAL,
                             child_noncritical.capabilities + [Action.MANAGE])
admin_noncritical = Ontology(
    UserLevel.ADMIN, DeviceClass.NONCRITICAL, adult_noncritical.capabilities)


ontologies = [visitor_critical, child_critical, adult_critical,
              admin_critical, visitor_noncritical, child_noncritical, adult_noncritical, admin_noncritical]


configuration_component = ConfigurationComponent(
    3, 24, 32, devices, users, ontologies)
ontology_component = OntologyComponent(configuration_component)
context_component = ContextComponent()
activity_component = ActivityComponent()
notification_component = NotificationComponent()
authorization_component = AuthorizationComponent(
    configuration_component, ontology_component, context_component, activity_component, notification_component)


# Authorization Component


id_req = 0
# 174,809 lines of records, 2 months, 60 days, 1 line per second
with open('d6_2m_0tm.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    last_state = None
    limit_date = None
    for row in spamreader:
        current_state = list(map(int, row[:NUMBER_OF_DEVICES]))
        if current_state == last_state:
            continue
        current_date = datetime.strptime(row[DATE_COL], '%Y-%m-%d %H:%M:%S')

        # room = next(
        #     room for room in act_room if ActivityEnum[row[29].upper()] in room["activities"])
        # print(row[29] + " -> " + str(room["id"]) + " - " + row[30])
        act = Activity(ActivityEnum[row[ACTIVITY_COL].upper()])
        # if act_window.empty() or act.activity is not act_window.queue[act_window.qsize() - 1].activity:
        #     if act_window.full():
        #         act_window.get()
        #     act_window.put(act)
        # print(act_window.queue)

        if last_state is not None:
            changes = [(i, e1, e2) for i, (e1, e2) in enumerate(
                zip(last_state, current_state)) if e1 != e2]
            # print("Changes:")
            # print(changes)
            for change in changes:
                if devices[change[0]].active:
                    print(current_date, act)
                    id_req += 1
                    req = Request(id_req, devices[change[0]], users[0], Context(
                        AccessWay.PERSONAL, Localization.INTERNAL, Time.COMMOM, Age.ADULT, Group.ALONE), Action.CONTROL)
                    authorization_component.on_request(
                        req, current_state, last_state, current_date)
                    print()

        last_state = current_state
