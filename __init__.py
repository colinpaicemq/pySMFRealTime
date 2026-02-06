from . import dumphex
import ctypes
from ctypes import *
import pathlib


#import json

class pySMFRT:
    def __enter__(self):
        self.conn(self.name)
        # turn self
        #return self.conn(self.name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disc()

    ####################################################################################################################
    # Iterators
    ####################################################################################################################
    def __iter__(self):
        return self

    def __next__(self):
        ret = self.get()
        if not ret:
            raise StopIteration
        return ret

    def __init__(self, name: str, debug=0):
        
        lib_file = pathlib.Path(__file__).parent / "pySMFRealTime.so"
        self.lib = ctypes.CDLL(str(lib_file))

        self.lib.conn.argtypes = [c_char_p,  # the name of stream
                                  c_char_p,  # the returned buffer
                                  #ctypes.POINTER(ctypes.c_int), # rc
                                  #ctypes.POINTER(ctypes.c_int), # rs 
                                  ctypes.POINTER(ctypes.c_int), # debug
                                ] 
        self.lib.conn.restype = c_int
        
        self.lib.get.argtypes = [ c_char_p,  # the token
                                  c_char_p,  # the returned buffer
                                  ctypes.POINTER(ctypes.c_int), # lBuffer
                                  c_char, # flag 
                                  #ctypes.POINTER(ctypes.c_int), # rc
                                  #ctypes.POINTER(ctypes.c_int), # rs
                                  ctypes.POINTER(ctypes.c_int), # debug 
                                  ] 
        self.lib.disc.argtypes = [c_char_p,  # the token
                                  #ctypes.POINTER(ctypes.c_int), # rc
                                  #ctypes.POINTER(ctypes.c_int), # rs
                                  ctypes.POINTER(ctypes.c_int), # debug 
                                  ] 
        self.lib.get.restype = c_int
        if debug is True:
            self.debug = 1
        elif debug is False:
            self.debug = 0
        else:
            self.debug = debug    
        #self.handle = None
        self.token = None     
        self.name = name


    ####################################################################################################################
    # Wrapper functions
    ####################################################################################################################
    def mystrerror(self,value):
        errorText = {
            0:"OK",
            0x0c02:"x0c02 SMF not active", 
            0x0c03:"x0c03 Storage obtain error", 
            0x0401:"x0401 Records skipped", 
            0x0402:"x0402 In Mem removed", 
            0x0403:"x0403 No data available", 
            0x0404:"x0404 Get already in progress", 
            0x0405:"0x405 Get already in progress",
            0x0406:"x0406 Get when Disc in progress", 
            0x0407:"x0407 Disconnect in progress", 
            0x0408:"x0408 Get while disc in progress", 
            0x0801:"x0801 Bad mode ", 
            0x0801:"x0801 Incorrect mode", 
            0x0802:"x0802 Parmlist control block problems", 
            0x0803:"x0803 No connection", 
            0x0804:"x0804 Bad token", 
            0x0805:"x0805 Unsupported operation", 
            0x0806:"x0806 Buffer too small", 
            0x0807:"x0807 No such resource", 
            0x0808:"x0808 Query buffer too small ", 
        }
        if value in errorText:
            return_value = errorText[value]
        else :
            return_value ="x{:x} Unknown reason code"
        return return_value
              
    

    #############################
    # conn
    # ##########################
    def conn(self,name: str,debug=None):
        """
        
        """
    
        token =  ctypes.create_string_buffer(16) # 16 byte handle
        #rc = ctypes.c_int(0)
        #rs = ctypes.c_int(0)
        if debug is None:            
            idebug = ctypes.c_int(self.debug)
        else :
            idebug = ctypes.c_int(debug)
        self.token = None
        retcode  = self.lib.conn(name.encode("cp500"),
                                    token,
                                    #rc,
                                    #rs,
                                    idebug)
        ret_string = self.mystrerror(retcode)
        if debug is not None:
            print("==conn",retcode,ret_string)
        if retcode != 0:
            #print("returned rc",rc, "reason",rs)
            print(">>>>>>>>>>>>>>>>> connect error ", ret_string)
            return None
        # print("returned rc",rc, "reason",rs)
        self.token = token
        return retcode
    ################
    # get
    ################
    #def get(self,flag=0):
    def get(self,wait=True,debug=None):
        # dumphex(self.token)

        
        if self.token is None:
            print("There is no token")
            return "","x0803 No connection"

        if wait is True:
            flag = 0x00
        else:
            flag = 0x10
        if debug is None:            
            idebug = ctypes.c_int(self.debug)
        else :
            idebug = ctypes.c_int(debug)
        #self.token = None
        lBuffer =32768
        buffer=  ctypes.create_string_buffer(lBuffer) #
        clBuffer =  ctypes.c_int(lBuffer)
        debug = ctypes.c_int(self.debug)
        retcode = self.lib.get(self.token,
                          buffer,
                          clBuffer,
                          flag,
                          #rc,
                          #rs,
                          debug)
        ret_string = self.mystrerror(retcode)
        print("get returned rc",ret_string, ". length",clBuffer.value)

        llBuffer = clBuffer.value
        if clBuffer.value == 0:
            v = ""
           #print("++++++ return",v,ret_string)
            return v, ret_string
        else :
            #print("--------")
            return buffer.raw[0:llBuffer], ret_string
        


    ###########################
    # Query
    ###########################    
    def query(self, debug=None):
        """
        
        """  
        if debug is None:            
            idebug = ctypes.c_int(self.debug)
        else :
            idebug = ctypes.c_int(debug)
        rc = self.lib.query(idebug)   


    ################
    # disc
    ################
    #def get(self,flag=0):
    def disc(self,):
        if self.debug > 0:
            print("Enter disc")

        if self.token is None:
            print("There is no token")
            return 0
        debug = ctypes.c_int(self.debug)
        rc = ctypes.c_int(0)
        rs = ctypes.c_int(0)
        #  print("self.token",self.token)
        rcr = self.lib.disc(self.token,
                          rc,
                          rs,
                          debug)

        # print("returned rc",rcr,rc, "reason",rs)
        self.token = None
        return rs
    
    ##########
    ## query
    #######
    def query(self,debug=None): 
        if debug is None:            
            idebug = ctypes.c_int(self.debug)
        else :
            idebug = ctypes.c_int(debug)
        rc = self.lib.query(debug)   


  