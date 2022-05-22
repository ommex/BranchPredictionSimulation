class two_bit_branch_prediction:
    def __init__(self):
        self.two_bit_prediction_data = {}
        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0

    def two_bit_bitwise_increment(self, bit):
        integer = int(bit, 2)
        if (integer < 3):
            return bin(integer + 1)
        else:
            return bit

    def two_bit_bitwise_decrement(self, bit):
        integer = int(bit, 2)
        if (integer > 0):
            return bin(integer - 1)
        else:
            return bit

    def two_bit_predict(self, address):
        if address in self.two_bit_prediction_data.keys():
            index = int(self.two_bit_prediction_data[address], 2)

            if index > 1:
                return True

            else:
                return False

        else:
            self.two_bit_prediction_data[address] = None
            return None

    def two_bit_save(self, address, branch):
        if self.two_bit_prediction_data[address] == None:
            self.new = self.new + 1
            if branch:
                self.two_bit_prediction_data[address] = bin(2)
            else:
                self.two_bit_prediction_data[address] = bin(0)

        else:
            if branch:

                bin_index = self.two_bit_prediction_data[address]
                bin_index = self.two_bit_bitwise_increment(bin_index)
                self.two_bit_prediction_data[address] = bin_index

            else:

                bin_index = self.two_bit_prediction_data[address]
                bin_index = self.two_bit_bitwise_decrement(bin_index)
                self.two_bit_prediction_data[address] = bin_index

    def two_bit_check(self, branch, prediction):
        if branch == prediction:
            self.right_cont = self.right_cont + 1
        else:
            self.wrong_count = self.wrong_count + 1

    def iterator(self, traces):

        self.whole_len = len(traces)

        for data in traces:
            branch_addr = data["branch_address"]
            branch = data["branch"]

            prediction = self.two_bit_predict(branch_addr)
            self.two_bit_save(branch_addr, branch)
            self.two_bit_check(branch, prediction)

        wrong_percentage = self.wrong_count / self.whole_len
        right_percentage = self.right_cont / self.whole_len

        return {"right": self.right_cont, "wrong": self.wrong_count, "whole": self.whole_len, "unique": self.new,
                "wrong_percentage": wrong_percentage, "right_percentage": right_percentage}
