'''
Process SMF 42 subtype 6 SMF records
'''
#import struct
#from collections import OrderedDict
# import pandas as pd
import  smfobjects as q




import pick

#def fields():
#    fields = ["Subsys","Header.hStarttime","Header,oDataset.datasetName"]
#    return fields

def process():
    '''
    main ( and only ) processing
    '''

    product = [q.xs(n="PL",l=8),
                q.xs(n="PN",l=10),
                q.xu(n="Subtype",l=1),
                q.xu(n="reserved",l=1,p="no",i=True,),
                q.xSTCK(n="StartTime"),
                q.xSTCK(n="EndTime"),
                q.xs(n="Reserved",l=4,p="No",i=True,),

    ]
    typelist ={0:"Other",1:"PS",2:"PDS",3:"PDSE",4:"DA",
               5:"ISAM",6:"EXCP",7:"Extended physical sequential data set",
               10:"HFS",16:"KSDS data component",17:"KSDS index component",
               18:"Variable RRDS data component",19:"Variable RRDS index component",
               20:"Fixed length RRDS",21:"Linear",22:"ESDS"}
    entrydesc = [[0x80,0x80,"First entry since open"],
                 ]
    entrytype = [[0xc0,0xc0,"GSR"],
                 [0xc0,0x80,"LSR"],
                 [0xc0,0x40,"RLS"],
                 [0xc0,0x00,"NSR"],
                 [0x10,0x10,"Open for EXCP"],
                 [0x80,0x80,"Non VSAM fixed length"],
                 [0x40,0x40,"Program library"],
                 [0x20,0x20,"Extended format"],
                 [0x01,0x01,"Compressed format"]
                 ]
    datasetIO = [q.x128(n="AvgRespTime"),
                q.x128(n="AvgConnTime"),
                q.x128(n="AvgPendTime"),
                q.x128(n="AvgDiscTime"),
                q.x128(n="AvgCUQTime"),
                q.xu(n="CountIO",l=4),
                q.xu(n="CacheCand",l=4),
                q.xu(n="CacheHits",l=4),
                q.xu(n="CacheWrCand",l=4),
                q.xu(n="CacheWrHits",l=4,o=36),
                q.xu(n="SeqIO",l=4),
                q.xu(n="RecLeveCacheOps",l=4),
                q.xu(n="InhibitCacheLoad",l=4),
                q.x128(n="AvgDAO",o=52),
                q.xu(n="MaxDSIORespTime",l=4),
                q.xu(n="ServiceTime",l=4),
                q.xu(n="ReadDiscTime",l=4),
                q.xu(n="ReadCount",l=4,o=68),
                q.xu(n="zHPFReads",l=4),
                q.xu(n="zHPWrites",l=4),
                q.xu(n="AvgRespuS",l=4,o=80),
                #q.xu(n="AvgRespuS",l=4),
                q.xu(n="AvgConnuS",l=4),
                q.xu(n="AvgPenduS",l=4),
                q.xu(n="AvgDiscuS",l=4,o=92),
                q.xu(n="AvgCUQuS",l=4,o=96),
                q.xu(n="AvgDAOuS",l=4,o=100),
                q.xu(n="AvgReadDiscuS",l=4),
                q.xu(n="AvgBusyuS",l=4),
                q.xu(n="AvgICRuS",l=4,o=112),
    ]
    ams =   [q.xu(n="SeqReadBlocks",l=4),
             q.xu(n="SeqReadDelay",l=4,o=4),
             q.xu(n="SeqWriteBlocks",l=4),
             q.xu(n="SeqWriteDelay",l=4),
             q.xu(n="DirectReadNumBlocks",l=4),
             q.x128(n="DirectReadTotDelay"),
             q.xu(n="DirectWriteNumBlocks",l=4),
             q.x128(n="DirectWriteTotalDelay",o=28),
             # q.xu(n="SeqWriteDelay",l=4),
             q.xu(n="DtyReads",l=4),
             q.x128(n="DtyReadDelay"),
             q.xu(n="DtyWrites",l=4),
             q.x128(n="DtyWriteDelay",o=44),
             q.xu(n="BytesRead",l=8),
             q.xu(n="BytesWritten",l=8),
             q.xu(n="BytesDecryptedRead",l=8,o=64),
             q.xu(n="VSAMCIRead",l=4),
             q.xu(n="VSAMCIWritten",l=4),
             ]
    dataset =[q.xu(n="offset",l=4),
              q.xs(n="datasetName",l=44,strip=True,),
              q.xu(n="datasetType",l=1,x=q.lookup,x0=typelist),
              q.xu(n="entryDescriptor",l=1,x=q.bitmask,x0=entrydesc),
              q.xu(n="datasetDescriptor",l=1,x=q.bitmask,x0=entrytype),
              q.xb(n="Reserved",l=1,i=True,),
              q.xoffset(n="odsio",t=datasetIO,ol=152),
              q.xoffset(n="oams",t=ams,ol=88,o=56),
        ]

    header   = [q.xs(n="JobName",l=8),
              q.SMFTime(n="hStarttime",o=8),
              q.SMFDate(n="hStartDate"),
              q.xs(n="Userid",l=8),
              q.xoffset(n="ODataset",t=dataset,ol=112),
              q.xu(n="lDataset",l=2,v=112)  # verify the lengths match
             ]



    opts = [q.xu(n="RecLen",c="RecordLength",l=2,i=True,),
            q.xu(n="Seg",c="Segment",l=2,o=2,i=True,),
            q.xx(n="Flag",c="",l=1),
            q.xu(n="RecordType",c="",l=1),
            q.SMFTime(n="Time",c=""),
            q.SMFDate(n="Date",c=""),
            q.xs(n="SID",c="",l=4),
            q.xs(n="Subsys",c="",l=4),
            q.xu(n="RecordSubType",c="",l=2,o=22),
            q.xu(n="Triplets",c="",l=2,o=24),
            q.xu(n="Reserved",p="No",l=2,i=True),
            q.xu(n="Product",l=8,i=True),
            #q.xtriplet(n="Product",t=product),
            q.xtriplet(n="Header",o=36,t=header),
    ]
    return opts
##########################################################
class smf():
    '''
    Main work done with a class; a class instance is passed back to the caller
    '''
    def __init__(self):
        self.name = ""
        self.rows = []

    def process(self):
        '''' call the function to return the options'''
        return process()

    def type_subType(self):
        '''
        Return type/suubtype
        '''
        return  "42/6"

    def doit(self,data):
        '''
        This is passed the data dict and we then process it
        '''
        #print("=smf42",data)
        #for x,xx in data.items():
        #    print("==149",x,xx)
        fields = ["Header.hStarttime","Header.JobName","Header.ODataset.datasetName",
                        "Header.ODataset.datasetType","Header.Userid",
                        "Header.ODataset.oams.BytesRead",
                        "Header.ODataset.odsio.AvgRespTime"]

        print("==155",data)
        o = pick.pick(data,fields)
        self.rows.extend(o)
    def  end(self):
        '''
        This is called after the end of reading all the records
        We can now process what we have saved
        '''
        print("SMF 42")
        pd.set_option("display.max_columns", None)
        pd.set_option('max_colwidth', 70)
        pd.set_option('display.max_rows', None)
        pd.options.display.width = 1000
        df = pd.DataFrame.from_records(self.rows)
        #df2 = df.sort_values('pathname',axis=0)
        print(df)


def init():
    '''
    This creates an instance of the smf class and returns it so we
    can call it and pass data etc
    '''
    s= smf()
    return s

