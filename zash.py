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
class Activity(Enum):
    SLEEP = 1
    PERSONAL = 2
    EAT = 3
    LEISURE = 4
    OTHER = 5
    ANOMALY = 6


@unique
class Action(Enum):
    VISUALIZE = 1
    ONOFF = 2
    MANAGE = 3


@unique
class DeviceClass(Enum):
    CRITICAL = 1
    NONCRITICAL = 2


@unique
class UserLevel(Enum):
    ADMIN = 1
    ADULT = 2
    CHILD = 3
    VISITOR = 4

@unique
class AccessWay(Enum):
    PERSONAL = 1
    HOUSE = 2
    REQUESTED = 3


@unique
class Localization(Enum):
    EXTERNAL = 1
    INTERNAL = 2


@unique
class Time(Enum):
    MORNING = 1
    AFTERNOON = 2
    NIGHT = 3


@unique
class Age(Enum):
    KID = 1
    TEEN = 2
    ADULT = 3


@unique
class Group(Enum):
    ALONE = 1
    TOGETHER = 2


act_room = [
    {"id": Room.BEDROOM, "activities": [Activity.SLEEP]},
    {"id": Room.BATHROOM, "activities": [Activity.PERSONAL]},
    {"id": Room.KITCHEN, "activities": [Activity.EAT]},
    {"id": Room.LIVINGROOM, "activities": [Activity.LEISURE]},
    {"id": Room.UNKOWN, "activities": [Activity.OTHER, Activity.ANOMALY]}
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
    def __init__(self, Activity):
        self.Activity = Activity

    def __repr__(self):
        return str(self.Activity)

    def __str__(self):
        return self.Activity


class Context:
    def __init__(self, access_way, localization, time, age, group):
        self.access_way = access_way
        self.localization = localization
        self.time = time
        self.age = age
        self.group = group


class User:
    def __init__(self, id, user_level):
        self.id = id
        self.user_level = user_level


class Device:
    def __init__(self, id, device_class, room):
        self.id = id
        self.device_class = device_class
        self.room = room


class Request:
    def __init__(self, device, user, ):
        self.id = id
        self.device_class = device_class
        self.room = room


# def on_request():


act_window = queue.Queue(WINDOW_SIZE)

with open('d6_2m_0tm.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    for row in spamreader:
        room = next(
            room for room in act_room if Activity[row[29].upper()] in room["activities"])
        print(row[29] + " -> " + str(room["id"]) + " - " + row[30])
        act = Activity(Activity[row[29].upper()])
        if act_window.empty() or act.Activity is not act_window.queue[act_window.qsize() - 1].Activity:
            if act_window.full():
                act_window.get()
            act_window.put(act)
            print(act_window.queue)

        if row[30] == "2016-03-03 18:30:31":
