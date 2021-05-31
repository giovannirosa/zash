class ConfigurationComponent:
    def __init__(self, block_threshold: int, block_interval: int, build_interval: int, devices: list, users: list, ontologies: list):
        self.block_threshold = block_threshold
        self.block_interval = block_interval
        self.build_interval = build_interval
        self.devices = devices
        self.users = users
        self.ontologies = ontologies

    def set_block_threshold(self, block_threshold: int):
        self.block_threshold = block_threshold

    def set_block_interval(self, block_interval: int):
        self.block_interval = block_interval

    def set_build_interval(self, build_interval: int):
        self.build_interval = build_interval

    def set_devices(self, devices: int):
        self.devices = devices

    def set_users(self, users: int):
        self.users = users

    def set_ontologies(self, ontologies: int):
        self.ontologies = ontologies