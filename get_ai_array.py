import numpy
import json
import numpy as np
from tqdm import tqdm
from pprint import pprint
from copy import deepcopy

history_len = 5


def setup_data(traces):
    data = []
    addresses = []

    for trace in tqdm(traces):

        address = trace["branch_address"]
        branch = trace["branch"]

        if address not in addresses:
            addresses.append(address)
            stack_pointer = 0
            history = []

            for i in range(history_len):
                history.append(False)

            tmp = [address, history, branch, stack_pointer]

            data.append(tmp)

            if address == "b77be7ab":
                continue

        else:
            for el in data[::-1]:
                if el[0] == address:
                    last_data = el[1]
                    last_branch = el[2]
                    stack_pointer = el[3]
                    break

            history = deepcopy(last_data)

            history[stack_pointer] = last_branch

            if stack_pointer < history_len - 1:
                stack_pointer = stack_pointer + 1

            tmp = [address, history, branch, stack_pointer]

            data.append(tmp)

    return data


filename = "checkpoint.json"

with open(filename, "r") as f:
    traces = json.load(f)

data = setup_data(traces["trace"])
