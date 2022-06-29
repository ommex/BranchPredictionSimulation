import local_iterators
import global_iterators
import hybrid_iterators
import predictor_test
from os import path

#hybrid_iterators.gshare_size_iterator(20, "trace", checkpoint="checkpoint.json", show=True)
#local_iterators.pht_size_iterator(20, "trace", checkpoint="checkpoint.json", high_res=False)
#local_iterators.pht_size_iterator(4, "trace", checkpoint="checkpoint.json", bit_crop=0, high_res=False)
#local_iterators.bit_crop_size_iterator(4, "trace", checkpoint="checkpoint.json",high_res=True)
#hybrid_iterators.tournament_global_history_iterator(13, 4, 2, 22, "trace", checkpoint="checkpoint.json", show=True, high_res=False)
#hybrid_iterators.tournament_bit_crop_iterator(4, 4, 2, 18, "trace", checkpoint="checkpoint.json", show=True, high_res=False)


def single_value_runner():
    print("Wilkommen beim Simulationsprogramm für Prädiktoren der Branch Prediction\n")
    print("Um bei wiederholter Ausführung schneller zu sein werden die .txt trace files einmal eingelesen und zu einem Checkpoint verarbeitet.")
    print("Bitte geben Sie jetzt den relativen Pfad zum Ordner an indem diese gespeichert sind. Für 'trace' ENTER")
    folder = input()
    if folder == "":
        folder = "trace"

    if not path.exists(folder):
        raise FileNotFoundError

    print("Nun kann der Prädiktor 0-3 ausgewählt werden \n0: localer n-bit predictor \n1: two level global predictor \n2: Gshare hybrid predictor\n3: Tournament hybrid predictor")
    predictor_i = int(input())

    print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
    pht_size = input()
    if pht_size == "":
        pht_size = 2
    else:
        pht_size = int(pht_size)

    if(predictor_i in [0, 3]):
        print("Geben sie ein wie viele Bits von links einer Adresse entfernt werden sollen. Für 10 Bit die übrig bleiben wäre es z.B. 32-10=22 \nFor example: 111100 with bitcrop 2 -> 1100\nfür 0 ENTER")
        bit_crop = input()
        if bit_crop == "":
            bit_crop = 0
        else:
            bit_crop = int(bit_crop)


        if(predictor_i==0):
            print("Running local_predictor for PHT-size: "+str(pht_size)+" BitCrop: "+str(bit_crop))
            predictor_test.test_local_predictor(folder, "checkpoint.json", pht_size, bit_crop)
        else:
            print("Geben sie die Länge in Bit der Globalen Historie ein.\nFür 2 ENTER")
            global_history_len = input()
            if global_history_len == "":
                global_history_len = 2
            else:
                global_history_len = int(global_history_len)

            print("Geben sie die Länge in Bit der Lokalen Historie ein.\nFür 2 ENTER")
            local_history_len = input()
            if local_history_len == "":
                local_history_len = 2
            else:
                local_history_len = int(local_history_len)


            print("Running tournament_predictor für globale_history_len: "+str(global_history_len)+" local_history_len: "+str(local_history_len)+" Pht-size: "+str(pht_size)+" BitCrop: "+str(bit_crop))
            predictor_test.test_tournament_predictor(folder, "checkpoint.json", global_history_len, local_history_len, pht_size, bit_crop)


    else:

        print("Geben sie die Länge in Bit der Globalen Historie ein.\nFür 2 ENTER")
        global_history_len = input()
        if global_history_len == "":
            global_history_len = 2
        else:
            global_history_len = int(global_history_len)

        if(predictor_i==1):
            print("Running two_level_global predictor mit Pht-size: "+str(pht_size)+" history_len: "+str(global_history_len))
            predictor_test.test_ght_predictor(folder, "checkpoint.json", pht_size, global_history_len)
        else:
            print("Running gshare predictor mit pht-size: "+str(pht_size)+" history_len: "+str(global_history_len))
            predictor_test.test_gshare_predictor(folder, "checkpoint.json", pht_size, global_history_len)

single_value_runner()

##FAQ
##What is bitcrop?
##Bitcrop is is number of binary digits the programm cuts of of the left side of the address:
##for example: 111100 with bitcrop 2 -> 1100
##But warning the programm fills empty zeros up to the architecture definded!
##so a bit crop of 2 with architecture 32bit of 0028f3d0 is still x28f3d0