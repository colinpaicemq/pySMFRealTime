def dumphex(indata:bytes):
    if indata is None:
        return 
    print("INDATA",type(indata),len(indata))
    out = ""
    ascii = ""
    ebcdic = ""
    start = 0
    EBCDIC = ''.join(( "................",
            "................", 
            "................",
            "................", 
            " .........¢.<(+|",
            "&.........!$*);⍺", 
            "-/........¦,%_>?",
            ".........`:#@'=\"", 
            ".abcdefghi......",
            ".jklmnopqr......", 
            ".~stuvwxyz...[..",
            ".............]..", 
            "{ABCDEFGHI......",
            "}JKLMNOPQR......", 
            "\\.STUVWXYZ......",
            "0123456789......"  ) )
    ASCII  = ''.join(("................" ,
            "................" , 
            " !\"#¢%&'()*+,-./" , 
            "0123456789:;<=>?" , 
            "@ABCDEFGHIJKLMNO" ,
            "PQRSTUVWXYZ∇\\∆∇_" , 
            "'abcdefghijklmno" , 
            "pqrstuvwxyz{ }~." , 
            "................" , 
            "................" , 
            "................" , 
            "................" , 
            "................" , 
            "................" , 
            "................" , 
            "................" ))
    print("ASCII",len(ASCII))
    for n, v in enumerate(indata):
        #print(n,v)
        iv = int.from_bytes(v) 
        out = out + "{0:x}".format(iv)
        # '{:02X}'.format
        
        ascii = ascii + ASCII[iv]
        ebcdic = ebcdic + EBCDIC[iv]
        # print("n",n%4,n,len(out),out)

        if n%4 == 3 and len(out) > 3 :
            out = out + " "
        if n%16 == 15 and len(out) > 16:
            print("{:08x}: {:<36}  {:<16}  {:<16}".format(start,out,ascii,ebcdic))  
            #print(out)
            out = ""
            ascii = ""
            ebcdic = ""
            start = n
    print("{:08x}: {:<36}  {:<16}  {:<16}".format(start,out,ascii,ebcdic))
    return ""
