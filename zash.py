import csv
import queue
from datetime import datetime, timedelta
from markov_zash import MarkovChain
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
           Device(4, DeviceClass.NONCRITICAL, Room.OFFICE, True),  # officeLight
           Device(5, DeviceClass.CRITICAL, Room.OFFICE, True),  # officeDoorLock
           Device(6, DeviceClass.NONCRITICAL, Room.OFFICE, True),  # officeDoor
           Device(7, DeviceClass.NONCRITICAL, Room.OFFICE, False),  # officeCarp
           Device(8, DeviceClass.NONCRITICAL, Room.OFFICE, False),  # office
           Device(9, DeviceClass.CRITICAL, Room.HOUSE, True),  # mainDoorLock
           Device(10, DeviceClass.NONCRITICAL, Room.HOUSE, True),  # mainDoor
           Device(11, DeviceClass.NONCRITICAL, Room.LIVINGROOM, True),  # livingLight
           Device(12, DeviceClass.NONCRITICAL, Room.LIVINGROOM, False),  # livingCarp
           Device(13, DeviceClass.NONCRITICAL, Room.KITCHEN, True),  # kitchenLight
           Device(14, DeviceClass.CRITICAL, Room.KITCHEN, True),  # kitchenDoorLock
           Device(15, DeviceClass.NONCRITICAL, Room.KITCHEN, True),  # kitchenDoor
           Device(16, DeviceClass.NONCRITICAL, Room.KITCHEN, False),  # kitchenCarp
           Device(17, DeviceClass.NONCRITICAL, Room.HOUSE, True),  # hallwayLight
           Device(18, DeviceClass.CRITICAL, Room.KITCHEN, True),  # fridge
           Device(19, DeviceClass.NONCRITICAL, Room.LIVINGROOM, False),  # couch
           Device(20, DeviceClass.NONCRITICAL, Room.BEDROOM, True),  # bedroomLight
           Device(21, DeviceClass.CRITICAL, Room.BEDROOM, True),  # bedroomDoorLock
           Device(22, DeviceClass.NONCRITICAL, Room.BEDROOM, True),  # bedroomDoor
           Device(23, DeviceClass.NONCRITICAL, Room.BEDROOM, False),  # bedroomCarp
           Device(24, DeviceClass.NONCRITICAL, Room.BEDROOM, True),  # bedTableLamp
           Device(25, DeviceClass.NONCRITICAL, Room.BEDROOM, False),  # bed
           Device(26, DeviceClass.NONCRITICAL, Room.BATHROOM, True),  # bathroomLight
           Device(27, DeviceClass.CRITICAL, Room.BATHROOM, True),  # bathroomDoorLock
           Device(28, DeviceClass.NONCRITICAL, Room.BATHROOM, True),  # bathroomDoor
           Device(29, DeviceClass.NONCRITICAL, Room.BATHROOM, False)]  # bathroomCarp


act_window = queue.Queue(WINDOW_SIZE)
requests = [{"time": "2016-03-03 18:30:31", "req": Request(1, devices[8], users[4], Context(
    AccessWay.REQUESTED, Localization.INTERNAL, Time.UNCOMMOM, Age.KID, Group.ALONE), Action.CONTROL)}]

suspect_list = []
blocked_list = []
block_threshold = 3
block_interval = 24
markov_build_interval = 32
past_days = 0
is_markov_building = True

markov_chain = MarkovChain()

def send_message(user: User, message: str):
    print("User {} received message: '{}'".format(user.id, message))


# Authorization Component
# checks for:
#   - Ontology Component
#   - Context Component
#   - Activity Component
# in order, and blocks user if failed enough within interval
def on_request(req: Request, current_state, last_state, current_date):
    print("Authorization Component")
    print("Processing Request: {}".format(str(req)))
    if req.user.blocked:
        print("USER IS BLOCKED - Request is NOT authorized!")
        return False
    if not verify_user_device(req) or not verify_context(req) or not verify_activities(current_state, last_state):
        req.user.rejected.append(current_date)
        print("User have now {} rejected requests!".format(len(req.user.rejected)))
        if len(req.user.rejected) > block_threshold:
            req.user.blocked = True
            print("User {} is blocked!".format(req.user))
            for user in users:
                send_message(user, "User {} is blocked!".format(req.user))
        print("Request is NOT authorized!")
        return False
    print("Request is authorized!")
    return True


# Ontology Component
# common ontologies like:
#   - critical devices:
#       - visitor cannot even visualize
#       - kids can only visualize
#       - adults can only visualize and control
#       - admins can visualize, control and manage
#   - non-critical devices:
#       - visitor and kids can visualize and control
#       - adults and admins can visualize, control and manage
def verify_user_device(req: Request):
    print("Ontology Component")
    print("Verify User Level {} with the Action {} on the device class {}".format(
        req.user.user_level, req.action, req.device.device_class))
    compatible = True
    if req.device.device_class is DeviceClass.CRITICAL:
        if (req.action is Action.MANAGE and req.user.user_level.value[0] > 1) or \
            (req.action is Action.CONTROL and req.user.user_level.value[0] > 2) or \
                (req.action is Action.VIEW and req.user.user_level.value[0] > 3):
            compatible = False
    else:
        if (req.action is Action.MANAGE and req.user.user_level.value[0] > 2):
            compatible = False
    str_result = 'compatible'
    if not compatible:
        str_result = 'incompatible'
    print("User level {} is {} with the Action {} on the device class {}".format(
        req.user.user_level, str_result, req.action, req.device.device_class))
    return compatible


# Context Component
# static trust calculation based on expected
# for [DeviceClass x Action] and [UserLevel x Action]
# from [AccessWay, Localization, Time, Age, Group]
def verify_context(req: Request):
    print("Context Component")
    print("Verify context {}".format(req.context))
    expected_device = req.device.device_class.value[1] + req.action.value[1]
    expected_user = req.user.user_level.value[1] + req.action.value[1]
    if req.context.trust() < max(expected_device, expected_user):
        print("Trust level is BELOW expected!")
        return False
    print("Trust level is ABOVE expected!")
    return True


# Activity Component
# check next state probability using a Markov Chain
# updates transition matrix with successful requests
def verify_activities(current_state, last_state):
    print("Activity Component")
    print("Verify activities")
    print(last_state)
    print(current_state)
    if is_markov_building:
        markov_chain.build_transition(current_state, last_state)
        return True
    else:
        prob = markov_chain.get_probability(current_state, last_state)
        if prob > 0:
            markov_chain.build_transition(current_state, last_state)
            print("Activity is valid!")
            return True
        else:
            print("Activity is NOT valid!")
            return False

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
        if limit_date is None:
            limit_date = current_date + timedelta(days=markov_build_interval)
        elif is_markov_building and current_date > limit_date:
            is_markov_building = False
            print("Markov Chain stopped building transition matrix at {}".format(
                current_date))

        # room = next(
        #     room for room in act_room if ActivityEnum[row[29].upper()] in room["activities"])
        # print(row[29] + " -> " + str(room["id"]) + " - " + row[30])
        act = Activity(ActivityEnum[row[ACTIVITY_COL].upper()])
        if act_window.empty() or act.activity is not act_window.queue[act_window.qsize() - 1].activity:
            if act_window.full():
                act_window.get()
            act_window.put(act)
            # print(act_window.queue)
        
        # clean rejects occurred out of interval
        for user in users:
            user.rejected = [rej_date for rej_date in user.rejected if current_date - rej_date < timedelta(hours=block_interval)]

        if last_state is not None:
            changes = [(i, e1, e2) for i, (e1, e2) in enumerate(zip(last_state, current_state)) if e1 != e2]
            # print("Changes:")
            # print(changes)
            for change in changes:
                if devices[change[0]].active:
                    print(current_date, act)
                    id_req += 1
                    req = Request(id_req, devices[change[0]], users[0], Context(AccessWay.PERSONAL, Localization.INTERNAL, Time.COMMOM, Age.ADULT, Group.ALONE), Action.CONTROL)
                    on_request(req, current_state, last_state, current_date)
                    print()

        last_state = current_state
