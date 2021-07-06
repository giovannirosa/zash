from enum import Enum, unique

@unique
class Room(Enum):
    BEDROOM = 1
    BATHROOM = 2
    KITCHEN = 3
    LIVINGROOM = 4
    OFFICE = 5
    HOUSE = 6
    UNKOWN = 7


@unique
class ActivityEnum(Enum):
    SLEEP = 1
    PERSONAL = 2
    EAT = 3
    LEISURE = 4
    OTHER = 5
    ANOMALY = 6


@unique
class Time(Enum):
    MORNING = 1
    AFTERNOON = 2
    NIGHT = 3


@unique  # id, additional sec
class Action(Enum):
    MANAGE = 1, 40
    CONTROL = 2, 20
    VIEW = 3, 0


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
    INTERNAL = 1, 30
    EXTERNAL = 2, 10


@unique  # id, given sec
class TimeClass(Enum):
    COMMOM = 1, 20
    UNCOMMOM = 2, 10


@unique  # id, given sec
class Age(Enum):
    ADULT = 1, 30
    TEEN = 2, 20
    KID = 3, 10


@unique  # id, given sec
class Group(Enum):
    TOGETHER = 1, 10
    ALONE = 2, 0