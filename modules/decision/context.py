from models_zash import Request


class ContextComponent:
    # static trust calculation based on expected
    # for [DeviceClass x Action] and [UserLevel x Action]
    # from [AccessWay, Localization, Time, Age, Group]
    def verify_context(self, req: Request):
        print("Context Component")
        print("Verify context {}".format(req.context))
        expected_device = req.device.device_class.value[1] + \
            req.action.value[1]
        expected_user = req.user.user_level.value[1] + req.action.value[1]
        expected = max(expected_device, expected_user)
        print("Trust level is {} and expected is {}".format(
            req.context.trust(), expected))
        if req.context.trust() < expected:
            print("Trust level is BELOW expected!")
            return False
        print("Trust level is ABOVE expected!")
        return True