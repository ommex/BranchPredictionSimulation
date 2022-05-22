from os import listdir
import pprint
import json
import matplotlib.pyplot as plt


class n_bit_branch_prediction:
    def __init__(self, len):
        self.prediction_data = {}
        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0

        self.int_len = 0
        self.int_len = 2**len - 1

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

    def predict(self, address):
        if address in self.prediction_data.keys():
            index = self.prediction_data[address]

            if index > int(self.int_len/2):
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
                self.prediction_data[address] = round(self.int_len/2)
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

    def iterator(self, traces):

        self.whole_len = len(traces)

        for data in traces:
            branch_addr = data["branch_address"]
            branch = data["branch"]

            prediction = self.predict(branch_addr)
            self.save(branch_addr, branch)
            self.check(branch, prediction)

        wrong_percentage = round((self.wrong_count / self.whole_len)*100,3)
        right_percentage = round((self.right_cont / self.whole_len)*100,3)

        return {"right": self.right_cont, "wrong": self.wrong_count, "whole": self.whole_len, "unique": self.new,
                "wrong_percentage": wrong_percentage, "right_percentage": right_percentage}


class two_bit_branch_prediction:
    def __init__(self):
        self.two_bit_prediction_data = {}
        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0

    def two_bit_bitwise_increment(self, bit):
        integer = int(bit,2)
        if(integer < 3):
            return bin(integer+1)
        else:
            return bit

    def two_bit_bitwise_decrement(self, bit):
        integer = int(bit,2)
        if(integer > 0):
            return bin(integer-1)
        else:
            return bit


    def two_bit_predict(self, address):
        if address in self.two_bit_prediction_data.keys():
            index = int(self.two_bit_prediction_data[address],2)

            if index>1:
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

        return {"right":self.right_cont, "wrong":self.wrong_count, "whole":self.whole_len, "unique":self.new, "wrong_percentage":wrong_percentage, "right_percentage":right_percentage}


class TraceReader:
    def __init__(self, folder, checkpoint=""):
        self.folder = folder
        self.traces = {}

        if checkpoint != "":
            print("read checkpoint")
            self.read_checkpoint(checkpoint)
            print("reading complete")

        else:
            self.read_files()


    def read_files(self):
        files = listdir(self.folder)

        for file in files:
            print("Starting to read "+file)
            file_name = file.split(".")[0]

            trace_contend_raw = open(self.folder+"/"+file, "r").readlines()
            trace_contend = []
            for line in trace_contend_raw:
                one_trace = {}

                line = line.replace("\n","")
                line = line.split(" ")

                branch_address = line[0]
                branch_type_raw = line[1]

                if branch_type_raw == '0':
                    branch_type = False
                elif branch_type_raw == "1":
                    branch_type = True
                else:
                    branch_type = None

                one_trace["branch_address"] = branch_address
                one_trace["branch"] = branch_type

                trace_contend.append(one_trace)

            self.traces[file_name] = trace_contend

    def save_checkpoint(self, filename):
        with open(filename, "w") as outfile:
            json.dump(self.traces, outfile, indent=4)

    def read_checkpoint(self, filename):
        with open(filename, 'r') as f:
            self.traces = json.load(f)


def n_bit_plot_predictor(end_bit, folder_name, checkpoint=""):
    fig = plt.figure()
    ax = fig.add_subplot()

    reader = TraceReader(folder_name, checkpoint)
    sizes = {}

    for file in reader.traces.keys():
        print("looking at "+file)
        plot_data = [[],[]]

        for i in range(1, end_bit+1):
            plot_data[0].append(i)
            traces = reader.traces[file]
            n_bit_iterator = n_bit_branch_prediction(i)

            simulation_results = n_bit_iterator.iterator(traces)
            plot_data[1].append(simulation_results["wrong_percentage"])

            print(simulation_results)

        ax.plot(plot_data[0], plot_data[1], label=file)
        sizes[file] = simulation_results["whole"]

    size_str = ""

    for file in sizes.keys():
        size = sizes[file]
        size_str = size_str + file + " has length of " + str(size) + "\n"

    print(size_str)

    ax.set_ylabel("wrong_percentage")
    ax.set_xlabel("bit_storage")

    ax.text(2, 26, size_str)

    plt.legend()
    plt.savefig("./plots/till_"+str(end_bit)+".png")
    plt.show()


n_bit_plot_predictor(5, "trace", "checkpoint.json")