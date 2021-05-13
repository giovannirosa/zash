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
