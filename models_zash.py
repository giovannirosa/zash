from enums_zash import *


class Activity:
    def __init__(self, activity):
        self.activity = activity

    def __repr__(self):
        return str(self.activity)

    def __str__(self):
        return str(self.activity)


class Context:
    def __init__(self, access_way: AccessWay, localization: Localization, group: Group):
        self.access_way = access_way
        self.localization = localization
        self.time = None  # will be computed during request in context component
        self.group = group

    def __repr__(self):
        return "Context[{},{},{},{}]".format(str(self.access_way), str(self.localization), str(self.time), str(self.group))

    def __str__(self):
        return "Context[{},{},{},{}]".format(str(self.access_way), str(self.localization), str(self.time), str(self.group))


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
    def __init__(self, id: int, user_level: UserLevel, age: Age):
        self.id = id
        self.user_level = user_level
        self.age = age
        self.rejected = []
        self.start_interval = None
        self.blocked = False

    def __repr__(self):
        return "User[{},{},{}]".format(str(self.id), str(self.user_level), str(self.age))

    def __str__(self):
        return "User[{},{},{}]".format(str(self.id), str(self.user_level), str(self.age))


class Device:
    def __init__(self, id: int, name: str, device_class: DeviceClass, room: Room, active: bool):
        self.id = id
        self.name = name
        self.device_class = device_class
        self.room = room
        self.active = active

    def __repr__(self):
        return "Device[{},{},{},{}]".format(str(self.id), self.name, str(self.device_class), str(self.room))

    def __str__(self):
        return "Device[{},{},{},{}]".format(str(self.id), self.name, str(self.device_class), str(self.room))


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
