import ctypes
from ctypes import *
import pathlib
#import json
from struct import *
import dumphex
"""
   typedef struct querycb {                                                         
      char        Eyecatcher[4];  /* Eye catcher             0    */                   
      uint16_t    Length;         /* Length of the block     4    */                   
      char        Rsvd1[1];       /* Reserved                6    */                   
      uint8_t     Version;        /* Version number          7   */                    
      char        Flags[2];       /* Flags                   8    */                   
      uint16_t    Reserved8;      //   10                                              
      uint32_t    Count;  // number returned  12                                       
      uint32_t    lBuffer; // length of buffer 16                                      
      uint32_t    Reservedx ;    //              20                                    
      void        *pBuffer;      //              24                                    
                                                                                        
    } querycb;      
"""    
eyec = "QRPB".encode("cp500")  # char[4]
# print("type",type(eyec))
l = 32                         # uint16_t
res1 = 0                       # char[1] 
version = 1                    #
flags = 0                      # char[2]
res2 = 0                       # uint16_t
count = 0                      # uint32_t  
lBuffer = 256                 # uint32_t 
res3 = 0                       # uint32_t 
# pBuffer                      # void *  
pBuffer = ctypes.create_string_buffer(b'abcdefg1111111111111111',size=lBuffer)

pB =  ctypes.cast(pBuffer, ctypes.c_void_p)
p = pack("@4shbbhhiiiP", eyec,l,res1,version,flags,res2,count,lBuffer,res3,
pB.value)

lib_file = pathlib.Path(__file__).parent / "load.so"
lib = ctypes.CDLL(str(lib_file))
# p = pack(">hll", 1, 2,5)
lib.query.argtypes = [  c_char_p,                      #ctypes.POINTER(ctypes.c_int), # rc
                      ctypes.c_void_p
                    ]   

p1 = ctypes.c_int(4660) # x1234
p2 = ctypes.cast(p, ctypes.c_void_p)

retcode  = lib.query(pBuffer,p2)
print("pbuffer",len(pBuffer),len(pBuffer.raw))
exit(0)
#print(dir(pBuffer))
dumphex.dumphex(pBuffer.raw)
print(retcode)