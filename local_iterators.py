import matplotlib.pyplot as plt
import trace_reader
import predictors


def pht_size_iterator(pht_size, folder_name, save_file_name, checkpoint="", bit_crop=0):
    fig = plt.figure()
    ax = fig.add_subplot()

    reader = trace_reader.TraceReader(folder_name, checkpoint)
    sizes = {}

    for file in reader.traces.keys():
        print("looking at " + file)
        plot_data = [[], []]

        for i in range(1, pht_size + 1):
            plot_data[0].append(i)
            traces = reader.traces[file]
            n_bit_iterator = predictors.n_bit_local_predictor(i, bit_crop=bit_crop)

            simulation_results = n_bit_iterator.check_traces(traces)
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
    ax.set_xlabel("pht_size")

    ax.text(2, 26, size_str)

    plt.legend()
    plt.savefig(save_file_name + ".png")

    plt.show()

    print("SAVED to " + save_file_name)


def bit_crop_size_iterator(
    end_bit_crop, folder_name, save_file_name, checkpoint="", pht_size=20
):
    fig = plt.figure()
    ax = fig.add_subplot()

    reader = trace_reader.TraceReader(folder_name, checkpoint)
    sizes = {}

    for file in reader.traces.keys():
        print("looking at " + file)
        plot_data = [[], []]

        for i in range(0, end_bit_crop + 1):
            plot_data[0].append(i)
            traces = reader.traces[file]
            n_bit_iterator = predictors.n_bit_local_predictor(pht_size, bit_crop=i)

            simulation_results = n_bit_iterator.check_traces(traces)
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
    ax.set_xlabel("bit_crop")

    ax.text(5, 26, size_str)

    plt.legend()
    plt.savefig(save_file_name + ".png")

    plt.show()

    print("SAVED to " + save_file_name)
