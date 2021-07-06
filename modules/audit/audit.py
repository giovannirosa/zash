from datetime import datetime
from models_zash import Request


class AuditComponent:
    def __init__(self):
        self.ontology_fail = []
        self.context_fail = []
        self.activity_fail = []
        self.blocks = []
        self.attacks = []
        self.valid_proofs = []
        self.invalid_proofs = []
        self.req_number = 0
        self.req_granted = 0
        self.req_refused = 0


class AuditEvent:
    def __init__(self, time: datetime, req: Request) -> None:
        self.time = time
        self.req = req

    def __repr__(self):
        return "{} - {}\n".format(str(self.time), str(self.req))

    def __str__(self):
        return "{} - {}\n".format(str(self.time), str(self.req))
