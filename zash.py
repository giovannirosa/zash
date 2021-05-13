import csv
import queue
from datetime import datetime, timedelta
from markov_zash import MarkovChain
from enums_zash import *
from models_zash import *


WINDOW_SIZE = 5
NUMBER_OF_DEVICES = 28
ACTIVITY_COL = 29
DATE_COL = 30


act_window = queue.Queue(WINDOW_SIZE)
requests = [{"time": "2016-03-03 18:30:31", "req": Request(Device(1, DeviceClass.CRITICAL, Room.LIVINGROOM), User(1, UserLevel.VISITOR), Context(
    AccessWay.REQUESTED, Localization.INTERNAL, Time.UNCOMMOM, Age.KID, Group.ALONE), Action.CONTROL)}]

suspect_list = []
blocked_list = []
block_threshold = 3
block_interval = 24
markov_build_interval = 32
past_days = 0
is_markov_building = True

markov_chain = MarkovChain()


# Authorization Component
# checks for:
#   - Ontology Component
#   - Context Component
#   - Activity Component
# in order, and blocks user if failed enough within interval
def on_request(req, current_state, last_state):
    print("Processing Request: {}".format(str(req)))
    if not verify_user_device(req) or not verify_context(req) or not verify_activities(current_state, last_state):
        suspect = False
        # verify_impersonation()
        if suspect and req.user.id in suspect_list:
            blocked_list.append(req.user.id)
        elif suspect:
            suspect_list.append(req.user.id)


# Ontology Component
# common ontologies like:
#   - critical devices:
#       - visitor cannot even visualize
#       - kids can only visualize
#       - adults can only visualize and control
#       - admins can visualize, control and manage
#   - non-critical devices:
#       - visitor and kids can visualize and control
#       - adults and admins can visualize, control and manage
def verify_user_device(req):
    print("Verify user level and device class")
    compatible = True
    if req.device.device_class is DeviceClass.CRITICAL:
        if (req.action is Action.MANAGE and req.user.user_level.value[0] > 1) or \
            (req.action is Action.CONTROL and req.user.user_level.value[0] > 2) or \
                (req.action is Action.VISUALIZE and req.user.user_level.value[0] > 3):
            compatible = False
    else:
        if (req.action is Action.MANAGE and req.user.user_level.value[0] > 2):
            compatible = False
    if not compatible:
        print("User level {} is incompatible with the action {} on the device class {}".format(req.user.user_level, req.action, req.device.device_class))
    return compatible


# Context Component
# static trust calculation based on expected
# for [DeviceClass x Action] and [UserLevel x Action]
# from [AccessWay, Localization, Time, Age, Group]
def verify_context(req):
    print("Verify context")
    expected_device = req.device.device_class.value[1] + req.action.value[1]
    expected_user = req.user.user_level.value[1] + req.action.value[1]
    expected = expected_device if expected_device > expected_user else expected_user
    if req.context.trust() < expected:
        print("Trust level is below expected")
        return False
    return True


# Activity Component
# check next state probability using a Markov Chain
# updates transition matrix with successful requests
def verify_activities(current_state, last_state):
    print("Verify activities")
    if is_markov_building:
        markov_chain.build_transition(current_state, last_state)
    else:
        prob = markov_chain.get_probability(current_state, last_state)
        if prob > 0:
            markov_chain.build_transition(current_state, last_state)
            return True
        else:
            return False
    


# 174,809 lines of records, 2 months, 60 days, 1 line per second
with open('d6_2m_0tm.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    last_state = None
    limit_date = None
    for row in spamreader:
        current_date = datetime.strptime(row[DATE_COL], '%Y-%m-%d %H:%M:%S')
        if limit_date is None:
            limit_date = current_date + timedelta(days=markov_build_interval)
        elif is_markov_building and current_date > limit_date:
            is_markov_building = False
            print("Markov Chain stopped building transition matrix at {}".format(current_date))

        # room = next(
        #     room for room in act_room if ActivityEnum[row[29].upper()] in room["activities"])
        # print(row[29] + " -> " + str(room["id"]) + " - " + row[30])
        act = Activity(ActivityEnum[row[ACTIVITY_COL].upper()])
        current_state = row[:NUMBER_OF_DEVICES + 1]
        if act_window.empty() or act.activity is not act_window.queue[act_window.qsize() - 1].activity:
            if act_window.full():
                act_window.get()
            act_window.put(act)
            # print(act_window.queue)

        req = next((req for req in requests if req["time"] == row[DATE_COL]), None)
        if req is not None:
            on_request(req["req"], current_state, last_state)
        last_state = current_state
