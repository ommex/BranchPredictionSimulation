import json
from os import listdir, path


class TraceReader:
    def __init__(self, folder, checkpoint=""):
        self.folder = folder
        self.traces = {}

        if checkpoint != "":
            self.try_checkpoint(checkpoint)
            print("read checkpoint")
            self.read_checkpoint(checkpoint)
            print("reading complete")

        else:
            self.read_files()

    def read_files(self):
        files = listdir(self.folder)

        for file in files:
            print("Starting to read " + file)
            file_name = file.split(".")[0]

            trace_contend_raw = open(self.folder + "/" + file, "r").readlines()
            trace_contend = []
            for line in trace_contend_raw:
                one_trace = {}

                line = line.replace("\n", "")
                line = line.split(" ")

                branch_address = line[0]
                branch_type_raw = line[1]

                if branch_type_raw == "0":
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
        with open(filename, "r") as f:
            self.traces = json.load(f)

    def try_checkpoint(self, filename):
        if not path.exists(filename):
            self.read_files()
            self.save_checkpoint(filename)
