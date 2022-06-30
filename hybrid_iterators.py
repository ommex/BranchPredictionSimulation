import matplotlib.pyplot as plt
from numpy import savetxt
from numpy import array
import trace_reader
import predictors


def gshare_size_iterator(
    history_end_size, folder_name, save_file_name, pht_size=2, checkpoint=""
):
    fig = plt.figure()
    ax = fig.add_subplot()

    reader = trace_reader.TraceReader(folder_name, checkpoint)
    sizes = {}

    for file in reader.traces.keys():
        print("looking at " + file)
        plot_data = [[], []]

        for i in range(1, history_end_size + 1):
            plot_data[0].append(i)
            traces = reader.traces[file]
            n_bit_iterator = predictors.n_bit_gshare(i, pht_len=pht_size)

            simulation_results = n_bit_iterator.check_traces(traces)
            plot_data[1].append(simulation_results["wrong_percentage"])

            print(simulation_results)

        ax.plot(plot_data[0], plot_data[1], label=file)
        sizes[file] = simulation_results["whole"]

    ax.set_ylabel("wrong_percentage")
    ax.set_xlabel("history_size")

    plt.legend()
    plt.savefig(save_file_name + ".png")

    plt.show()

    print("SAVED to " + save_file_name)


def tournament_local_history_iterator(
    local_history_end_size,
    global_history_len,
    pht_len,
    bit_crop,
    folder_name,
    save_file_name,
    checkpoint="",
):
    fig = plt.figure()
    ax = fig.add_subplot()

    reader = trace_reader.TraceReader(folder_name, checkpoint)
    sizes = {}

    for file in reader.traces.keys():
        print("looking at " + file)
        plot_data = [[], []]

        for i in range(1, local_history_end_size + 1):
            plot_data[0].append(i)
            traces = reader.traces[file]
            n_bit_iterator = predictors.n_bit_tournament(
                i, global_history_len, pht_len=pht_len, bit_crop=bit_crop
            )

            simulation_results = n_bit_iterator.check_traces(traces)
            plot_data[1].append(simulation_results["wrong_percentage"])

            print(simulation_results)

        ax.plot(plot_data[0], plot_data[1], label=file)
        sizes[file] = simulation_results["whole"]

    ax.set_ylabel("wrong_percentage")
    ax.set_xlabel("local_history_size")

    plt.legend()
    plt.savefig(save_file_name + ".png")

    plt.show()

    print("SAVED to " + save_file_name)


def tournament_global_history_iterator(
    global_history_end_size,
    local_history_len,
    pht_len,
    bit_crop,
    folder_name,
    save_file_name,
    checkpoint="",
):
    fig = plt.figure()
    ax = fig.add_subplot()

    reader = trace_reader.TraceReader(folder_name, checkpoint)
    sizes = {}

    for file in reader.traces.keys():
        print("looking at " + file)
        plot_data = [[], []]

        for i in range(1, global_history_end_size + 1):
            plot_data[0].append(i)
            traces = reader.traces[file]
            n_bit_iterator = predictors.n_bit_tournament(
                i, local_history_len, pht_len=pht_len, bit_crop=bit_crop
            )

            simulation_results = n_bit_iterator.check_traces(traces)
            plot_data[1].append(simulation_results["wrong_percentage"])

            print(simulation_results)

        ax.plot(plot_data[0], plot_data[1], label=file)
        sizes[file] = simulation_results["whole"]

    ax.set_ylabel("wrong_percentage")
    ax.set_xlabel("global_history_size")

    plt.legend()
    plt.savefig(save_file_name + ".png")

    plt.show()

    print("SAVED to " + save_file_name)


def tournament_bit_crop_iterator(
    global_history_len,
    local_history_len,
    pht_len,
    end_bit_crop,
    folder_name,
    save_file_name,
    checkpoint="",
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
            n_bit_iterator = predictors.n_bit_tournament(
                global_history_len, local_history_len, pht_len=pht_len, bit_crop=i
            )

            simulation_results = n_bit_iterator.check_traces(traces)
            plot_data[1].append(simulation_results["wrong_percentage"])

            print(simulation_results)

        ax.plot(plot_data[0], plot_data[1], label=file)
        sizes[file] = simulation_results["whole"]

    ax.set_ylabel("wrong_percentage")
    ax.set_xlabel("bit_crop")

    plt.legend()
    plt.savefig(save_file_name + ".png")

    savetxt(save_file_name + ".csv", array(plot_data), delimiter=",")

    plt.show()

    print("SAVED to " + save_file_name)
