import local_iterators
import global_iterators
import hybrid_iterators


hybrid_iterators.gshare_size_iterator(20, "trace", checkpoint="checkpoint.json", show=True)
#global_iterators.history_size_iterator(20, "trace", checkpoint="checkpoint.json", high_res=False)
#local_iterators.pht_size_iterator(4, "trace", checkpoint="checkpoint.json", bit_crop=0, high_res=False)
#local_iterators.bit_crop_size_iterator(8, "trace", checkpoint="checkpoint.json",high_res=True)


##FAQ
##What is bitcrop?
##Bitcrop is is number of binary digits the programm cuts of of the left side of the address:
##for example: 111100 with bitcrop 2 -> 1100
##But warning the programm fills empty zeros up to the architecture definded!
##so a bit crop of 2 with architecture 32bit of 0028f3d0 is still x28f3d0