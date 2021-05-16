from enums_zash import *

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
