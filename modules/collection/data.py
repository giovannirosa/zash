from models_zash import Request


class DataComponent:
    def __init__(self):
        self.last_state = None
        self.current_state = None

    def update_current_state(self, req: Request):
        self.current_state = self.last_state[:]
        current_device_state = self.current_state[req.device.id - 1]
        self.current_state[req.device.id -
                           1] = 0 if current_device_state else 1

    def update_last_state(self):
        self.last_state = self.current_state
