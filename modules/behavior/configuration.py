class ConfigurationComponent:
    def __init__(self, block_threshold: int, block_interval: int, markov_build_interval: int, devices: list, users: list, ontologies: list):
        self.block_threshold = block_threshold
        self.block_interval = block_interval
        self.markov_build_interval = markov_build_interval
        self.devices = devices
        self.users = users
        self.ontologies = ontologies