import matplotlib.pyplot as plt
import trace_reader
import predictors


def history_size_iterator(
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
            n_bit_iterator = predictors.n_bit_global_two_level_predictor(
                i, pht_len=pht_size
            )

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
