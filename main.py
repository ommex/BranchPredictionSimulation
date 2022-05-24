from os import listdir
import pprint
import json
import matplotlib.pyplot as plt


class n_bit_branch_prediction:
    def __init__(self, len, bit_crop=0, architecture=32):
        self.prediction_data = {}
        self.right_cont = 0
        self.wrong_count = 0
        self.whole_len = 0
        self.new = 0

        self.int_len = 0
        self.int_len = 2**len - 1

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

    def crop_hex(self, hex_input, amount):
        if amount > 0:
            int_value = int(hex_input, base=16)
            bin_value = bin(int_value)
            bin_cropped = ""

            input_len = len(bin_value)

            for bit in range(amount - 1):
                bin_cropped = bin_value[input_len - bit - 1] + bin_cropped

            hex_cropped = hex(int(bin_cropped, 2))

            return hex_cropped

        else:
            return hex_input


    def predict(self, input_address):

        address = self.crop_hex(input_address, self.bit_crop)

        if address in self.prediction_data.keys():
            index = self.prediction_data[address]

            if index > int(self.int_len/2):
                return True

            else:
                return False

        else:
            self.prediction_data[address] = None
            return None


    def save(self, input_address, branch):
        address = self.crop_hex(input_address, self.bit_crop)

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


def n_bit_plot_predictor(end_bit, folder_name, checkpoint="", bit_crop=0, show=True):
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
            n_bit_iterator = n_bit_branch_prediction(i, bit_crop=bit_crop)

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

    save_file_name = "./plots/end_bit"+str(end_bit)+"_bit_crop_"+str(bit_crop)+".png"

    plt.legend()
    plt.savefig(save_file_name)
    if show:
        plt.show()

    print("SAVED to "+save_file_name)


for i in range(2, 21):
    n_bit_plot_predictor(20, "trace", checkpoint="checkpoint.json", bit_crop=i, show=False)
