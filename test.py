# Example showing how to connect to SMF Real Time 
import sys, locale, os
import pySMFRealTime
#print("dir",dir(smf))
a= pySMFRealTime . pySMFRT(debug=False)
print("Display what SMF REal Time are available")
a.query()

print("Test connect to an SMF Real Time definition")
x = a.conn("IFASMF.INMEM")
x = a.disc()
exit()
