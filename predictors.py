import collections

class n_bit_local_predictor:
    def __init__(self, pht_len, bit_crop=0, architecture=32):
        self.prediction_data = {}
        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0

        self.int_len = 2 ** pht_len - 1

        self.bit_crop = bit_crop
        self.architecture = architecture

    def increment(self, integer):
        if (integer < self.int_len):
            return integer + 1
        else:
            return integer

    def decrement(self, integer):
        if (integer > 0):
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

        return {"right": self.right_cont, "wrong": self.wrong_count, "whole": self.whole_len, "unique": self.new,
                "wrong_percentage": wrong_percentage, "right_percentage": right_percentage, "bit_crop": self.bit_crop,
                "sample_adress": branch_addr, "pht_size": self.int_len}

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

        self.get_binary = lambda x, n: format(x, 'b').zfill(n)

        self.init_pht_register()
        self.init_history()


    def init_pht_register(self):
        for i in range(2 ** self.history_len):
            self.pht_register[self.get_binary(i, self.history_len)] = 0

    def init_history(self):
        for i in range(self.history_len):
            self.history.append(0)

    def increment(self, integer):
        if (integer < 2):
            return integer + 1
        else:
            return integer

    def decrement(self, integer):
        if (integer > 0):
            return integer - 1
        else:
            return integer


    def predict(self):
        history_string = ''.join(str(e) for e in self.history)
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
            history_string = ''.join(str(e) for e in self.history)
            pht_value = self.pht_register[history_string]
            new_pht_value = self.increment(pht_value)
            self.pht_register[history_string] = new_pht_value


        else:
            history_string = ''.join(str(e) for e in self.history)
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

        return {"right": self.right_cont, "wrong": self.wrong_count, "whole": self.whole_len, "unique": self.new,
                "wrong_percentage": wrong_percentage, "right_percentage": right_percentage,
                "sample_adress": branch_addr, "pht_size": self.pht_len, "history_len":self.history_len}