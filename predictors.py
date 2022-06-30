import collections


class n_bit_local_predictor:
    def __init__(self, pht_len, bit_crop=0, architecture=32):
        self.prediction_data = {}
        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0

        self.int_len = 2**pht_len - 1

        self.bit_crop = bit_crop
        self.architecture = architecture

    def increment(self, integer):
        if integer < self.int_len:
            return integer + 1
        else:
            return integer

    def decrement(self, integer):
        if integer > 0:
            return integer - 1
        else:
            return integer

    def hex_2_binary(self, hex_input):
        int_value = int(hex_input, base=16)
        bin_value = bin(int_value)

        bin_value = bin_value.replace("0b", "")

        bin_len = len(bin_value)
        added_zeros = self.architecture - bin_len

        for i in range(added_zeros):
            bin_value = "0" + bin_value

        return bin_value

    def crop_hex(self, hex_input, amount):

        if amount > 0:
            amount = 32 - amount

            bin_value = self.hex_2_binary(hex_input)
            bin_cropped = ""

            input_len = len(bin_value)

            for bit in range(amount):
                bin_cropped = bin_value[input_len - bit - 1] + bin_cropped

            hex_cropped = hex(int(bin_cropped, 2))

            return hex_cropped

        else:
            return hex_input

    def predict(self, address):

        if address in self.prediction_data.keys():
            index = self.prediction_data[address]

            if index > int(self.int_len / 2):
                return True

            else:
                return False

        else:
            self.prediction_data[address] = None
            return None

    def save(self, address, branch):

        if self.prediction_data[address] == None:
            self.new = self.new + 1
            if branch:
                self.prediction_data[address] = round(self.int_len / 2)
            else:
                self.prediction_data[address] = 0

        else:
            if branch:

                index = self.prediction_data[address]
                index = self.increment(index)
                self.prediction_data[address] = index

            else:

                index = self.prediction_data[address]
                index = self.decrement(index)
                self.prediction_data[address] = index

    def check(self, branch, prediction):
        if branch == prediction:
            self.right_cont = self.right_cont + 1
        else:
            self.wrong_count = self.wrong_count + 1

    def check_traces(self, traces):

        self.whole_len = len(traces)

        for data in traces:
            raw_branch_addr = data["branch_address"]
            branch = data["branch"]

            branch_addr = self.crop_hex(raw_branch_addr, self.bit_crop)

            prediction = self.predict(branch_addr)
            self.save(branch_addr, branch)
            self.check(branch, prediction)

        wrong_percentage = round((self.wrong_count / self.whole_len) * 100, 3)
        right_percentage = round((self.right_cont / self.whole_len) * 100, 3)

        return {
            "right": self.right_cont,
            "wrong": self.wrong_count,
            "whole": self.whole_len,
            "unique": self.new,
            "wrong_percentage": wrong_percentage,
            "right_percentage": right_percentage,
            "bit_crop": self.bit_crop,
            "sample_adress": branch_addr,
            "pht_size": self.int_len,
        }


class n_bit_global_two_level_predictor:
    def __init__(self, history_len, pht_len=2):

        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0
        self.pht_len = pht_len

        self.history_len = history_len

        self.history = []
        self.pht_register = {}

        self.get_binary = lambda x, n: format(x, "b").zfill(n)

        self.init_pht_register()
        self.init_history()

    def init_pht_register(self):
        for i in range(2**self.history_len):
            self.pht_register[self.get_binary(i, self.history_len)] = 0

    def init_history(self):
        for i in range(self.history_len):
            self.history.append(0)

    def increment(self, integer):
        if integer < 2:
            return integer + 1
        else:
            return integer

    def decrement(self, integer):
        if integer > 0:
            return integer - 1
        else:
            return integer

    def predict(self):
        history_string = "".join(str(e) for e in self.history)
        pht_value = self.pht_register[history_string]

        if pht_value > int(self.pht_len / 2):
            return True

        else:
            return False

    def append_history(self, branch):
        value = 1 if branch else 0

        tmp_list = collections.deque(self.history)
        tmp_list.rotate(1)
        self.history = list(tmp_list)
        self.history[0] = value

    def save(self, branch):

        if branch:
            history_string = "".join(str(e) for e in self.history)
            pht_value = self.pht_register[history_string]
            new_pht_value = self.increment(pht_value)
            self.pht_register[history_string] = new_pht_value

        else:
            history_string = "".join(str(e) for e in self.history)
            pht_value = self.pht_register[history_string]
            new_pht_value = self.decrement(pht_value)
            self.pht_register[history_string] = new_pht_value

        self.append_history(branch)

    def check(self, branch, prediction):
        if branch == prediction:
            self.right_cont = self.right_cont + 1
        else:
            self.wrong_count = self.wrong_count + 1

    def check_traces(self, traces):
        self.whole_len = len(traces)

        for data in traces:
            branch_addr = data["branch_address"]
            branch = data["branch"]

            prediction = self.predict()
            self.save(branch)
            self.check(branch, prediction)

        wrong_percentage = round((self.wrong_count / self.whole_len) * 100, 3)
        right_percentage = round((self.right_cont / self.whole_len) * 100, 3)

        return {
            "right": self.right_cont,
            "wrong": self.wrong_count,
            "whole": self.whole_len,
            "unique": self.new,
            "wrong_percentage": wrong_percentage,
            "right_percentage": right_percentage,
            "sample_adress": branch_addr,
            "pht_size": self.pht_len,
            "history_len": self.history_len,
        }


class n_bit_tournament:
    def __init__(
        self,
        local_history_len,
        global_history_len,
        pht_len=2,
        bit_crop=0,
        architecture=32,
    ):
        self.decision_dict = {}

        self.local_history = {}
        self.local_pht_register = {}
        self.global_history = []
        self.global_pht_register = {}

        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0

        self.pht_len = 2**pht_len - 1
        self.local_history_len = local_history_len
        self.global_history_len = global_history_len

        self.bit_crop = bit_crop
        self.architecture = architecture

        self.get_binary = lambda x, n: format(x, "b").zfill(n)

        self.init_pht_register()
        self.init_global_history()

    def init_pht_register(self):
        for i in range(2**self.global_history_len):
            self.global_pht_register[self.get_binary(i, self.global_history_len)] = 0

        for i in range(2**self.local_history_len):
            self.local_pht_register[self.get_binary(i, self.local_history_len)] = 0

    def init_global_history(self):
        for i in range(self.global_history_len):
            self.global_history.append(0)

    def increment(self, integer):
        if integer < self.pht_len:
            return integer + 1
        else:
            return integer

    def decrement(self, integer):
        if integer > 0:
            return integer - 1
        else:
            return integer

    def hex_2_binary(self, hex_input):
        int_value = int(hex_input, base=16)
        bin_value = self.get_binary(int_value, self.architecture)

        return bin_value

    def crop_hex(self, hex_input, amount):

        if amount > 0:
            amount = 32 - amount

            bin_value = self.hex_2_binary(hex_input)
            bin_cropped = ""

            input_len = len(bin_value)

            for bit in range(amount):
                bin_cropped = bin_value[input_len - bit - 1] + bin_cropped

            hex_cropped = hex(int(bin_cropped, 2))

            return hex_cropped

        else:
            return hex_input

    def predict_local(self, address):

        if address in self.local_history.keys():
            local_history = self.local_history[address]
            pht_address = "".join(str(x) for x in local_history)
            pht_value = self.local_pht_register[pht_address]

            if pht_value > int(self.pht_len / 2):
                return True

            else:
                return False

        else:
            return False

    def predict_global(self):

        history_string = "".join(str(e) for e in self.global_history)
        pht_value = self.global_pht_register[history_string]

        if pht_value > int(self.pht_len / 2):
            return True

        else:
            return False

    def decider(self, address):
        if address in self.decision_dict:
            return self.decision_dict[address]
        else:
            self.decision_dict[address] = False
            return None

    def save_decider(self, address, decision):
        if not decision:
            self.decision_dict[address] = not self.decision_dict[address]

    def append_history(self, input_history, branch):
        value = 1 if branch else 0

        tmp_list = collections.deque(input_history)
        tmp_list.rotate(1)
        output_history = list(tmp_list)
        output_history[0] = value

        return output_history

    def save_local(self, address, branch):

        if address not in self.local_history.keys():
            self.new = self.new + 1

            start_history = []
            for i in range(self.local_history_len):
                start_history.append(0)

        else:
            start_history = self.local_history[address]

        appended_history = self.append_history(start_history, branch)
        self.local_history[address] = appended_history

        pht_address = "".join(str(x) for x in start_history)

        if branch:

            index = self.local_pht_register[pht_address]
            index = self.increment(index)
            self.local_pht_register[pht_address] = index

        else:

            index = self.local_pht_register[pht_address]
            index = self.decrement(index)
            self.local_pht_register[pht_address] = index

    def save_global(self, branch):

        if branch:
            history_string = "".join(str(e) for e in self.global_history)
            pht_value = self.global_pht_register[history_string]
            new_pht_value = self.increment(pht_value)
            self.global_pht_register[history_string] = new_pht_value

        else:
            history_string = "".join(str(e) for e in self.global_history)
            pht_value = self.global_pht_register[history_string]
            new_pht_value = self.decrement(pht_value)
            self.global_pht_register[history_string] = new_pht_value

        new_history_string = self.append_history(history_string, branch)
        new_history = []
        for el in new_history_string:
            new_history.append(el)

        self.global_history = new_history

    def check(self, branch, prediction):
        if branch == prediction:
            self.right_cont = self.right_cont + 1
            return True
        else:
            self.wrong_count = self.wrong_count + 1
            return False

    def check_traces(self, traces):

        self.whole_len = len(traces)

        for data in traces:
            raw_branch_addr = data["branch_address"]
            branch = data["branch"]
            predictor_type = self.decider(raw_branch_addr)
            cropped_branch_addr = self.crop_hex(raw_branch_addr, self.bit_crop)

            if predictor_type:
                prediction = self.predict_local(cropped_branch_addr)

            else:
                prediction = self.predict_global()

            self.save_local(cropped_branch_addr, branch)
            self.save_global(branch)
            decision = self.check(branch, prediction)

            self.save_decider(raw_branch_addr, decision)

        wrong_percentage = round((self.wrong_count / self.whole_len) * 100, 3)
        right_percentage = round((self.right_cont / self.whole_len) * 100, 3)

        return {
            "right": self.right_cont,
            "wrong": self.wrong_count,
            "whole": self.whole_len,
            "unique": self.new,
            "wrong_percentage": wrong_percentage,
            "right_percentage": right_percentage,
            "bit_crop": self.bit_crop,
            "sample_address": branch,
            "pht_size": self.pht_len,
        }


class n_bit_gshare:
    def __init__(self, history_len, pht_len=2, architecture=32):

        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0
        self.pht_len = pht_len

        self.history_len = history_len
        self.architecture = architecture

        self.history = []
        self.pht_register = {}

        self.get_binary = lambda x, n: format(x, "b").zfill(n)

        self.init_pht_register()
        self.init_history()

    def init_pht_register(self):
        for i in range(2**self.history_len):
            self.pht_register[self.get_binary(i, self.history_len)] = 0

    def init_history(self):
        for i in range(self.history_len):
            self.history.append(0)

    def increment(self, integer):
        if integer < 2:
            return integer + 1
        else:
            return integer

    def decrement(self, integer):
        if integer > 0:
            return integer - 1
        else:
            return integer

    def xor(self, a, b, n):
        ans = ""

        # Loop to iterate over the
        # Binary Strings
        for i in range(n):

            # If the Character matches
            if a[i] == b[i]:
                ans += "0"
            else:
                ans += "1"
        return ans

    def hex_2_binary(self, hex_input):
        int_value = int(hex_input, base=16)
        bin_value = self.get_binary(int_value, self.architecture)

        return bin_value

    def get_back_bits(self, hex_input, len):
        bin_input = self.hex_2_binary(hex_input)
        bin_array = []

        for bit in bin_input[::-1]:
            bin_array.append(bit)

            len -= 1
            if len == 0:
                break

        bin_output = "".join(str(e) for e in bin_array[::-1])

        return bin_output

    def predict(self, address):
        history_string = "".join(str(e) for e in self.history)
        address_last_bits = self.get_back_bits(address, self.history_len)

        hybrid_bits = self.xor(history_string, address_last_bits, self.history_len)

        pht_value = self.pht_register[hybrid_bits]

        if pht_value > int(self.pht_len / 2):
            return True

        else:
            return False

    def append_history(self, branch):
        value = 1 if branch else 0

        tmp_list = collections.deque(self.history)
        tmp_list.rotate(1)
        self.history = list(tmp_list)
        self.history[0] = value

    def save(self, branch, address):
        address_last_bits = self.get_back_bits(address, self.history_len)
        history_string = "".join(str(e) for e in self.history)

        hybrid_bits = self.xor(history_string, address_last_bits, self.history_len)

        if branch:
            pht_value = self.pht_register[hybrid_bits]
            new_pht_value = self.increment(pht_value)
            self.pht_register[hybrid_bits] = new_pht_value

        else:
            pht_value = self.pht_register[hybrid_bits]
            new_pht_value = self.decrement(pht_value)
            self.pht_register[hybrid_bits] = new_pht_value

        self.append_history(branch)

    def check(self, branch, prediction):
        if branch == prediction:
            self.right_cont = self.right_cont + 1
        else:
            self.wrong_count = self.wrong_count + 1

    def check_traces(self, traces):
        self.whole_len = len(traces)

        for data in traces:
            branch_addr = data["branch_address"]
            branch = data["branch"]

            prediction = self.predict(branch_addr)
            self.save(branch, branch_addr)
            self.check(branch, prediction)

        wrong_percentage = round((self.wrong_count / self.whole_len) * 100, 3)
        right_percentage = round((self.right_cont / self.whole_len) * 100, 3)

        return {
            "right": self.right_cont,
            "wrong": self.wrong_count,
            "whole": self.whole_len,
            "wrong_percentage": wrong_percentage,
            "right_percentage": right_percentage,
            "sample_adress": branch_addr,
            "pht_size": self.pht_len,
            "history_len": self.history_len,
        }
