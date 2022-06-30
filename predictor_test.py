import trace_reader
import predictors


def open_traces(folder_name, checkpoint):
    reader = trace_reader.TraceReader(folder_name, checkpoint)
    traces = reader.traces
    return traces


def test_local_predictor(folder_name, checkpoint, pht_size, bit_crop):
    output = []
    traces = open_traces(folder_name, checkpoint)

    for fname in traces.keys():
        file = traces[fname]

        print("file: " + str(fname))

        local_predictor = predictors.n_bit_local_predictor(pht_size, bit_crop=bit_crop)
        simulation_results = local_predictor.check_traces(file)
        output.append(simulation_results)
        print(simulation_results)

    return output


def test_ght_predictor(folder_name, checkpoint, pht_size, history_len):
    output = []
    traces = open_traces(folder_name, checkpoint)

    for fname in traces.keys():
        file = traces[fname]

        print("file: " + str(fname))

        global_predictor = predictors.n_bit_global_two_level_predictor(
            history_len, pht_size
        )
        simulation_results = global_predictor.check_traces(file)
        output.append(simulation_results)
        print(simulation_results)

    return output


def test_gshare_predictor(folder_name, checkpoint, pht_size, history_len):
    output = []
    traces = open_traces(folder_name, checkpoint)

    for fname in traces.keys():
        file = traces[fname]

        print("file: " + str(fname))

        global_predictor = predictors.n_bit_gshare(history_len, pht_len=pht_size)
        simulation_results = global_predictor.check_traces(file)
        output.append(simulation_results)
        print(simulation_results)

    return output


def test_tournament_predictor(
    folder_name, checkpoint, global_history_len, local_history_len, pht_len, bit_crop
):
    output = []
    traces = open_traces(folder_name, checkpoint)

    for fname in traces.keys():
        file = traces[fname]

        print("file: " + str(fname))

        global_predictor = predictors.n_bit_tournament(
            local_history_len, global_history_len, pht_len=pht_len, bit_crop=bit_crop
        )
        simulation_results = global_predictor.check_traces(file)
        output.append(simulation_results)
        print(simulation_results)

    return output
