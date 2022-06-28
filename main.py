import local_iterators
import global_iterators
import hybrid_iterators
import predictor_test


#print("Local 2-Bit ohne Bitcrop")
#predictor_test.test_local_predictor("trace", "checkpoint.json", 2, 0)

#print("GHT 2-Bit ohne Bitcrop history:4 pht:2")
#predictor_test.test_ght_predictor("trace", "checkpoint.json", 2, 4)

#print("Gshare history:4 pht:2")
#predictor_test.test_gshare_predictor("trace", "checkpoint.json", 2, 4)

print("tournament global_history:4 local_history:4 local pht: 2 bitcrop 20")
predictor_test.test_tournament_predictor("trace", "checkpoint.json", 4, 4, 2, 0)


#hybrid_iterators.gshare_size_iterator(20, "trace", checkpoint="checkpoint.json", show=True)
#local_iterators.pht_size_iterator(20, "trace", checkpoint="checkpoint.json", high_res=False)
#local_iterators.pht_size_iterator(4, "trace", checkpoint="checkpoint.json", bit_crop=0, high_res=False)
#local_iterators.bit_crop_size_iterator(4, "trace", checkpoint="checkpoint.json",high_res=True)


##FAQ
##What is bitcrop?
##Bitcrop is is number of binary digits the programm cuts of of the left side of the address:
##for example: 111100 with bitcrop 2 -> 1100
##But warning the programm fills empty zeros up to the architecture definded!
##so a bit crop of 2 with architecture 32bit of 0028f3d0 is still x28f3d0