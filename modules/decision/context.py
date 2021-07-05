import datetime
from modules.audit.audit import AuditComponent, AuditEvent
from modules.behavior.configuration import ConfigurationComponent
from enums_zash import Action, Time, TimeClass, UserLevel
from models_zash import Context, Request, User
import operator
from typing import Callable


class ContextComponent:
    def __init__(self, configuration_component: ConfigurationComponent, audit_component: AuditComponent) -> None:
        self.configuration_component = configuration_component
        self.is_time_building = True
        self.limit_date = None
        self.audit_component = audit_component
        # {device, user_level, action, total_occ, times}
        self.time_prob_list = []
        for device in configuration_component.devices:
            for ul in UserLevel:
                for act in Action:
                    self.time_prob_list.append(
                        {"device": device, "user_level": ul, "action": act, "total_occ": 0, "times": [{"time": Time.MORNING, "percentage": 0, "occurrences": 0},
                                                                                                      {"time": Time.AFTERNOON,
                                                                                                      "percentage": 0, "occurrences": 0},
                                                                                                      {"time": Time.NIGHT, "percentage": 0, "occurrences": 0}]})

    # static trust calculation based on expected
    # for [DeviceClass x Action] and [UserLevel x Action]
    # from [AccessWay, Localization, Time, Age, Group]
    def verify_context(self, req: Request, current_date: datetime, explicit_authentication: Callable) -> bool:
        print("Context Component")
        self.calculate_time(req, current_date)
        self.check_building(current_date)
        if self.is_time_building:
            print("Time probability is still building")
            req.context.time = TimeClass.COMMOM
        print("Verify context {} with {} in {}".format(
            req.context, req.user, current_date))
        expected_device = req.device.device_class.value[1] + \
            req.action.value[1]
        expected_user = req.user.user_level.value[1] + req.action.value[1]
        expected = min(max(expected_device, expected_user), 100)
        calculated = min(self.calculate_trust(req.context, req.user), 100)
        print("Trust level is {} and expected is {}".format(
            calculated, expected))
        if calculated < expected:
            self.audit_component.context_fail.append(
                AuditEvent(current_date, req))
            print("Trust level is BELOW expected! Requires proof of identity!")
            if not explicit_authentication(req, current_date):
                return False
        print("Trust level is ABOVE expected!")
        return True

    # check if time build expired
    def check_building(self, current_date: datetime):
        if self.limit_date is None:
            self.limit_date = current_date + \
                datetime.timedelta(
                    days=self.configuration_component.build_interval)
        elif self.is_time_building and current_date > self.limit_date:
            self.is_time_building = False
            print("Time context stopped building probabilities at {}".format(
                current_date))

    def calculate_trust(self, context: Context, user: User):
        return context.access_way.value[1] + context.localization.value[1] + context.time.value[1] + user.age.value[1] + context.group.value[1]

    def calculate_time(self, req: Request, current_date: datetime):
        time = None
        if current_date.time() >= datetime.time(6) and current_date.time() < datetime.time(12):
            time = Time.MORNING
        elif current_date.time() >= datetime.time(12) and current_date.time() < datetime.time(18):
            time = Time.AFTERNOON
        elif (current_date.time() >= datetime.time(18) and current_date.time() <= datetime.time(23, 59, 59)) or \
                (current_date.time() >= datetime.time(0) and current_date.time() < datetime.time(6)):
            time = Time.NIGHT

        time_prob = next((time_prob for time_prob in self.time_prob_list if time_prob["device"] ==
                          req.device and time_prob["user_level"] == req.user.user_level and time_prob["action"] == req.action), None)

        self.recalculate_probabilities(time_prob, time)

        match_time = next(
            time_rec for time_rec in time_prob["times"] if time_rec["time"] == time)
        if match_time["percentage"] < 0.3:
            req.context.time = TimeClass.UNCOMMOM
        else:
            req.context.time = TimeClass.COMMOM
        # max_time = max(time_prob['times'],
        #                key=operator.itemgetter('percentage'))
        # if max_time["time"] == time:
        #     req.context.time = TimeClass.COMMOM
        # else:
        #     req.context.time = TimeClass.UNCOMMOM

    def recalculate_probabilities(self, time_prob: dict, time: Time):
        time_prob["total_occ"] += 1
        for time_rec in time_prob["times"]:
            if time_rec["time"] == time:
                time_rec["occurrences"] += 1
            time_rec["percentage"] = time_rec["occurrences"] / \
                time_prob["total_occ"]
