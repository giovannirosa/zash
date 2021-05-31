import datetime
from modules.behavior.configuration import ConfigurationComponent
from enums_zash import Time, TimeClass
from models_zash import Context, Request, User
import operator


class ContextComponent:
    def __init__(self, configuration_component: ConfigurationComponent) -> None:
        self.configuration_component = configuration_component
        self.is_time_building = True
        self.limit_date = None
        self.time_prob_list = []  # {device, times}
        for device in configuration_component.devices:
            self.time_prob_list.append(
                {"device": device, "total_occ": 0, "times": [{"time": Time.MORNING, "percentage": 0, "occurrences": 0},
                                                             {"time": Time.AFTERNOON,
                                                             "percentage": 0, "occurrences": 0},
                                                             {"time": Time.NIGHT, "percentage": 0, "occurrences": 0}]})

    # static trust calculation based on expected
    # for [DeviceClass x Action] and [UserLevel x Action]
    # from [AccessWay, Localization, Time, Age, Group]
    def verify_context(self, req: Request, current_date: datetime) -> bool:
        print("Context Component")
        self.calculate_time(req, current_date)
        self.check_building(current_date)
        print("Verify context {} with {} in {}".format(req.context, req.user, current_date))
        if self.is_time_building:
            return True
        expected_device = req.device.device_class.value[1] + \
            req.action.value[1]
        expected_user = req.user.user_level.value[1] + req.action.value[1]
        expected = max(expected_device, expected_user)
        calculated = self.calculate_trust(req.context, req.user)
        print("Trust level is {} and expected is {}".format(
            calculated, expected))
        if calculated < expected:
            print("Trust level is BELOW expected!")
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
        elif current_date.time() >= datetime.time(18) and current_date.time() < datetime.time(6):
            time = Time.NIGHT

        time_prob = next((time_prob for time_prob in self.time_prob_list if time_prob["device"] ==
                          req.device), None)

        self.recalculate_probabilities(time_prob, time)

        max_time = max(time_prob['times'], key=operator.itemgetter('percentage'))
        if max_time["time"] == time:
            req.context.time = TimeClass.COMMOM
        else:
            req.context.time = TimeClass.UNCOMMOM

    def recalculate_probabilities(self, time_prob: dict, time: Time):
        time_prob["total_occ"] += 1
        for time_rec in time_prob["times"]:
            if time_rec["time"] == time:
                time_rec["occurrences"] += 1
            time_rec["percentage"] = time_rec["occurrences"] / \
                time_prob["total_occ"]