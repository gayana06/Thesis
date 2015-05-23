#import subprocess
#from subprocess import Popen,PIPE
#output = Popen(["./a.out", "-f oracle_twitter"], stdout=PIPE).communicate()[0]
#print output
import ctypes
from ctypes import *

#libtest = cdll.LoadLibrary('/home/ubuntu/oracle_files/libsee5.so')
libtest=ctypes.CDLL('/home/ubuntu/ML_SERVER/libsee5.so')
#libtest -f oracle_twitter
libtest.initiateSee5withTrees("/home/ubuntu/ML_SERVER/oracle_twitter")
quorum=ctypes.c_char_p(libtest.getPrediction("5,178,20,0.00572598840772,0.0262176970641,79,12,?")) 
print('New Value = '+ quorum.value);
#libtest.print_string("olaaa\n")


#str = c_char_p(libtest.envia_string())

#print str.value
#str = c_char_p(libtest.getPrediction("x,2PC,0.84994147125,N/A,0.027968874749999997,N/A,1.47058200875,N/A,1.37E10,26238.125,N/A,10092.325,225.25,N/A,10320.8,N/A,643.99,6.5,6.5,3005.275,6.275,6.625,N/A,7141.0,3551.9249999999997,75.15,74.8518518525,1.0,?,w1-10"))

#print str.value
