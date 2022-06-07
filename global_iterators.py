import matplotlib.pyplot as plt
from numpy import savetxt
from numpy import array
import trace_reader
import predictors

def history_size_iterator(history_end_size, folder_name, pht_size=2, checkpoint="", show=True, high_res=False):
    fig = plt.figure()
    ax = fig.add_subplot()

    reader = trace_reader.TraceReader(folder_name, checkpoint)
    sizes = {}

    for file in reader.traces.keys():
        print("looking at "+file)
        plot_data = [[],[]]

        for i in range(1, history_end_size+1):
            plot_data[0].append(i)
            traces = reader.traces[file]
            n_bit_iterator = predictors.n_bit_global_two_level_predictor(i, pht_len=pht_size)

            simulation_results = n_bit_iterator.check_traces(traces)
            plot_data[1].append(simulation_results["wrong_percentage"])

            print(simulation_results)

        ax.plot(plot_data[0], plot_data[1], label=file)
        sizes[file] = simulation_results["whole"]

    ax.set_ylabel("wrong_percentage")
    ax.set_xlabel("history_size")


    save_file_name = "./plots/variable_history_size/pht_size_"+str(pht_size)+"_history_end_size_"+str(history_end_size)

    plt.legend()
    plt.savefig(save_file_name+".png")

    if high_res:
        savetxt(save_file_name+'.csv', array(plot_data), delimiter=',')

    if show:
        plt.show()

    print("SAVED to "+save_file_name)