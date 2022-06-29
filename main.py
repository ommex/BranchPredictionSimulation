import local_iterators
import global_iterators
import hybrid_iterators
import predictor_test
from os import path



def plotter_runner(folder):

    print("Geben sie einen reinen Dateinamen (ohne Dateiendung!) an wie die Tabelle heißen soll")
    save_file_name = input()

    if path.exists(save_file_name+".png"):
        print("A File with this name already exists!")
        raise ValueError


    print("Nun kann der Prädiktor 0-3 ausgewählt werden \n0: lokaler n-bit predictor \n1: two level global predictor \n2: Gshare hybrid predictor\n3: Tournament hybrid predictor")
    predictor_i = int(input())

    if predictor_i == 0:
        print("0: variable Adress Länge\n1: variable PHT Größe")
        local_predictor_mode = input()
        if local_predictor_mode == "0":
            print("Geben sie ein wie viele Bits von links einer Adresse maximal entfernt werden sollen. Für 10 Bit die übrig bleiben wäre es z.B. 32-10=22 \nFor example: 111100 with bitcrop 2 -> 1100")
            end_bit_crop = int(input())
            if end_bit_crop < 0 or end_bit_crop >= 32:
                print("Die Eingabe kann nur zwischen 0 und 32 liegen!")
                raise ValueError

            print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
            pht_size = input()
            if pht_size == "":
                pht_size = 2
            else:
                pht_size = int(pht_size)

            local_iterators.bit_crop_size_iterator(end_bit_crop, folder, save_file_name, checkpoint="checkpoint.json", pht_size=pht_size)

        elif local_predictor_mode == "1":
            print("Geben sie ein wie viele Bits von links einer Adresse entfernt werden sollen. Für 10 Bit die übrig bleiben wäre es z.B. 32-10=22 \nfür 0 ENTER")
            bit_crop = input()
            if bit_crop == "":
                bit_crop = 0
            else:
                bit_crop = int(bit_crop)

            if bit_crop < 0 or bit_crop >= 32:
                print("Die Eingabe kann nur zwischen 0 und 32 liegen!")
                raise ValueError

            print("Geben sie die maximale Größe der PHT Register in Bit an:")
            pht_size = int(input())

            local_iterators.pht_size_iterator(pht_size, folder, save_file_name, checkpoint="checkpoint.json", bit_crop=bit_crop)

    elif predictor_i == 1:
        print("Geben Sie die maximale Historylänge ein")
        history_end_size = int(input())

        print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
        pht_size = input()
        if pht_size == "":
            pht_size = 2
        else:
            pht_size = int(pht_size)

        global_iterators.history_size_iterator(history_end_size, folder, save_file_name, pht_size=pht_size, checkpoint="checkpoint.json")


    elif predictor_i == 2:

        print("Geben Sie die maximale Historylänge ein")
        history_end_size = int(input())

        print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
        pht_size = input()
        if pht_size == "":
            pht_size = 2
        else:
            pht_size = int(pht_size)

        hybrid_iterators.gshare_size_iterator(history_end_size, folder, save_file_name, pht_size=pht_size, checkpoint="checkpoint.json")


    elif predictor_i == 3:
        print("1: Variable Globale History\n2: Variable Lokale History\n3: Variable Adresslänge")
        tournament_mode = int(input())

        if tournament_mode == 1:
            print("Geben Sie die maximale Globale Historylänge ein")
            global_history_end_size = int(input())

            print("Geben sie die Länge in Bit der Lokalen Historie ein.\nFür 2 ENTER")
            local_history_len = input()
            if local_history_len == "":
                local_history_len = 2
            else:
                local_history_len = int(local_history_len)

            print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
            pht_size = input()
            if pht_size == "":
                pht_size = 2
            else:
                pht_size = int(pht_size)

            print(
                "Geben sie ein wie viele Bits von links einer Adresse entfernt werden sollen. Für 10 Bit die übrig bleiben wäre es z.B. 32-10=22 \nfür 0 ENTER")
            bit_crop = input()
            if bit_crop == "":
                bit_crop = 0
            else:
                bit_crop = int(bit_crop)

            if bit_crop < 0 or bit_crop >= 32:
                print("Die Eingabe kann nur zwischen 0 und 32 liegen!")
                raise ValueError

            hybrid_iterators.tournament_global_history_iterator(global_history_end_size, local_history_len, pht_size, bit_crop, folder, save_file_name, checkpoint="checkpoint.json")

        elif tournament_mode == 2:
            print("Geben sie die maximale Länge in Bit der Lokalen Historie ein.\nFür 2 ENTER")
            local_history_end_size = int(input())

            print("Geben sie die Länge in Bit der Globalen Historie ein.\nFür 2 ENTER")
            global_history_len = input()
            if global_history_len == "":
                global_history_len = 2
            else:
                global_history_len = int(global_history_len)

            print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
            pht_size = input()
            if pht_size == "":
                pht_size = 2
            else:
                pht_size = int(pht_size)

            print("Geben sie ein wie viele Bits von links einer Adresse entfernt werden sollen. Für 10 Bit die übrig bleiben wäre es z.B. 32-10=22 \nfür 0 ENTER")
            bit_crop = input()
            if bit_crop == "":
                bit_crop = 0
            else:
                bit_crop = int(bit_crop)

            if bit_crop < 0 or bit_crop >= 32:
                print("Die Eingabe kann nur zwischen 0 und 32 liegen!")
                raise ValueError


            hybrid_iterators.tournament_local_history_iterator(local_history_end_size, global_history_len, pht_size, bit_crop,
                                                  folder, save_file_name, checkpoint="checkpoint.json")


        elif tournament_mode == 3:
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

            print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
            pht_size = input()
            if pht_size == "":
                pht_size = 2
            else:
                pht_size = int(pht_size)

            print("Geben sie ein wie viele Bits von links einer Adresse maximal entfernt werden sollen. Für 10 Bit die übrig bleiben wäre es z.B. 32-10=22 \nfür 0 ENTER")
            bit_crop = input()
            if bit_crop == "":
                bit_crop = 0
            else:
                bit_crop = int(bit_crop)

            if bit_crop < 0 or bit_crop >= 32:
                print("Die Eingabe kann nur zwischen 0 und 32 liegen!")
                raise ValueError


            hybrid_iterators.tournament_bit_crop_iterator(global_history_len, local_history_len, pht_size, bit_crop, folder,
                                             save_file_name, checkpoint="checkpoint.json")


def single_value_runner(folder):
    print("Nun kann der Prädiktor 0-3 ausgewählt werden \n0: lokaler n-bit predictor \n1: two level global predictor \n2: Gshare hybrid predictor\n3: Tournament hybrid predictor")
    predictor_i = int(input())

    print("Geben sie die Größe der PHT Register in Bit an:\nfür 2 ENTER")
    pht_size = input()
    if pht_size == "":
        pht_size = 2
    else:
        pht_size = int(pht_size)


    if(predictor_i in [0, 3]):
        print("Geben sie ein wie viele Bits von links einer Adresse entfernt werden sollen. Für 10 Bit die übrig bleiben wäre es z.B. 32-10=22 \nfür 0 ENTER")
        bit_crop = input()
        if bit_crop == "":
            bit_crop = 0
        else:
            bit_crop = int(bit_crop)

        if bit_crop < 0 or bit_crop >= 32:
            print("Die Eingabe kann nur zwischen 0 und 32 liegen!")
            raise ValueError


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

if __name__ == '__main__':
    print("Wilkommen beim Simulationsprogramm für Prädiktoren der Branch Prediction\n")
    print("Um bei wiederholter Ausführung schneller zu sein werden die .txt trace files einmal eingelesen und zu einem Checkpoint verarbeitet.")
    print("Bitte geben Sie jetzt den relativen Pfad zum Ordner an indem diese gespeichert sind. Für 'trace' ENTER")
    folder = input()
    if folder == "":
        folder = "trace"

    if not path.exists(folder):
        raise FileNotFoundError


    print("1: Einzelwert Modus\n2: Tabellen Erstellungsmodus")
    mode = input()
    if mode == "1":
        single_value_runner(folder)
    if mode == "2":
        plotter_runner(folder)

##FAQ
##What is bitcrop?
##Bitcrop is is number of binary digits the programm cuts of of the left side of the address:
##for example: 111100 with bitcrop 2 -> 1100
##But warning the programm fills empty zeros up to the architecture definded!
##so a bit crop of 2 with architecture 32bit of 0028f3d0 is still x28f3d0