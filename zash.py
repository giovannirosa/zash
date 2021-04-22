import csv
import queue
from enum import Enum, unique


WINDOW_SIZE = 5


@unique
class Room(Enum):
    BEDROOM = 1
    BATHROOM = 2
    KITCHEN = 3
    LIVINGROOM = 4
    UNKOWN = 5


@unique
class ActivityEnum(Enum):
    SLEEP = 1
    PERSONAL = 2
    EAT = 3
    LEISURE = 4
    OTHER = 5
    ANOMALY = 6


@unique
class RequestTime(Enum):
    MORNING = 1
    AFTERNOON = 2
    NIGHT = 3


@unique  # id, additional sec
class Action(Enum):
    MANAGE = 1, 40
    CONTROL = 2, 20
    VISUALIZE = 3, 0


@unique  # id, initial sec
class DeviceClass(Enum):
    CRITICAL = 1, 30
    NONCRITICAL = 2, 0


@unique  # id, initial sec
class UserLevel(Enum):
    ADMIN = 1, 70
    ADULT = 2, 50
    CHILD = 3, 30
    VISITOR = 4, 0


@unique  # id, given sec
class AccessWay(Enum):
    REQUESTED = 1, 30
    HOUSE = 2, 20
    PERSONAL = 3, 10


@unique  # id, given sec
class Localization(Enum):
    INTERNAL = 1, 20
    EXTERNAL = 2, 10


@unique  # id, given sec
class Time(Enum):
    COMMOM = 1, 20
    UNCOMMOM = 1, 10


@unique  # id, given sec
class Age(Enum):
    ADULT = 1, 30
    TEEN = 2, 20
    KID = 3, 10


@unique  # id, given sec
class Group(Enum):
    TOGETHER = 1, 20
    ALONE = 2, 10


act_room = [
    {"id": Room.BEDROOM, "activities": [ActivityEnum.SLEEP]},
    {"id": Room.BATHROOM, "activities": [ActivityEnum.PERSONAL]},
    {"id": Room.KITCHEN, "activities": [ActivityEnum.EAT]},
    {"id": Room.LIVINGROOM, "activities": [ActivityEnum.LEISURE]},
    {"id": Room.UNKOWN, "activities": [
        ActivityEnum.OTHER, ActivityEnum.ANOMALY]}
]

# user_levels = {
#     "admin": 70,
#     "adult": 50,
#     "kid": 30,
#     "visitor": 0
# }

# device_classes = {
#     "critical": 70,
#     "non-critical": 50,
# }

# capabilities = {
#     "visualize": 0,
#     "on/off": 20,
#     "manage": 40,
# }

# access_way = {
#     "personal_device": 10,
#     "house_device": 20,
#     "required_device": 30
# }

# localization = {
#     "external": 10,
#     "proximities": 20,
#     "internal": 30
# }

# time = {
#     "morning": 10,
#     "afternoon": 20,
#     "night": 30
# }

# age = {
#     "kid": 10,
#     "teen": 20,
#     "adult": 30
# }

# group = {
#     "alone": 10,
#     "grouped": 20
# }


class Activity:
    def __init__(self, activity):
        self.activity = activity

    def __repr__(self):
        return str(self.activity)

    def __str__(self):
        return str(self.activity)


class Context:
    def __init__(self, access_way, localization, time, age, group):
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


class User:
    def __init__(self, id, user_level):
        self.id = id
        self.user_level = user_level

    def __repr__(self):
        return "User[{},{}]".format(str(self.id), str(self.user_level))

    def __str__(self):
        return "User[{},{}]".format(str(self.id), str(self.user_level))


class Device:
    def __init__(self, id, device_class, room):
        self.id = id
        self.device_class = device_class
        self.room = room

    def __repr__(self):
        return "Device[{},{},{}]".format(str(self.id), str(self.device_class), str(self.room))

    def __str__(self):
        return "Device[{},{},{}]".format(str(self.id), str(self.device_class), str(self.room))


class Request:
    def __init__(self, device, user, context, action):
        self.id = id
        self.device = device
        self.user = user
        self.context = context
        self.action = action

    def __repr__(self):
        return "Request[{},{},{},{},{}]".format(str(self.id), str(self.device), str(self.user), str(self.context), str(self.action))

    def __str__(self):
        return "Context[{},{},{},{},{}]".format(str(self.id), str(self.device), str(self.user), str(self.context), str(self.action))


act_window = queue.Queue(WINDOW_SIZE)
requests = [{"time": "2016-03-03 18:30:31", "req": Request(Device(1, DeviceClass.CRITICAL, Room.LIVINGROOM), User(1, UserLevel.VISITOR), Context(
    AccessWay.REQUESTED, Localization.INTERNAL, Time.UNCOMMOM, Age.KID, Group.ALONE), Action.CONTROL)}]

suspect_list = []
blocked_list = []


def on_request(req):
    print("Processing Request: {}".format(str(req)))
    if not verify_user_device(req) or not verify_context(req) or verify_activities(req):
        suspect = False
        # verify_impersonation()
        if suspect and req.user.id in suspect_list:
            blocked_list.append(req.user.id)
        elif suspect:
            suspect_list.append(req.user.id)


# common ontologies like:
#   - critical devices:
#       - visitor cannot even visualize
#       - kids can only visualize
#       - adults can only visualize and control
#       - admins can visualize, control and manage
#   - non-critical devices:
#       - visitor and kids can visualize and control
#       - adults and admins can visualize, control and manage
def verify_user_device(req):
    print("Verify user level and device class")
    compatible = True
    if req.device.device_class is DeviceClass.CRITICAL:
        if (req.action is Action.MANAGE and req.user.user_level.value > 1) or \
            (req.action is Action.CONTROL and req.user.user_level.value > 2) or \
                (req.action is Action.VISUALIZE and req.user.user_level.value > 3):
            compatible = False
            return False
    else:
        if (req.action is Action.MANAGE and req.user.user_level.value > 2):
            compatible = False
            return False
    if not compatible:
        print("User level is incompatible with the action on the device")
    return compatible


# static trust calculation based on expected
# for [DeviceClass x Action] and [UserLevel x Action]
# from [AccessWay, Localization, Time, Age, Group]
def verify_context(req):
    print("Verify context")
    expected_device = req.device.device_class.value[1] + req.action.value[1]
    expected_user = req.user.user_level.value[1] + req.action.value[1]
    expected = expected_device if expected_device > expected_user else expected_user
    if req.context.trust() < expected:
        print("Trust level is below expected")
        return False
    return True


# 
def verify_activities(req):
    print("Verify activities")
    last_act = act_window.queue[act_window.qsize() - 1].activity
    room = next(
        room for room in act_room if last_act in room["activities"])
    return True


# 174,809 lines of records, 2 months, 60 days, 1 line per second
with open('d6_2m_0tm.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    for row in spamreader:
        room = next(
            room for room in act_room if ActivityEnum[row[29].upper()] in room["activities"])
        print(row[29] + " -> " + str(room["id"]) + " - " + row[30])
        act = Activity(ActivityEnum[row[29].upper()])
        if act_window.empty() or act.activity is not act_window.queue[act_window.qsize() - 1].activity:
            if act_window.full():
                act_window.get()
            act_window.put(act)
            print(act_window.queue)

        req = next((req for req in requests if req["time"] == row[30]), None)
        if req is not None:
            on_request(req["req"])
