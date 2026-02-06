// Python interface to SMF Real Time.  C component
// /////////////////////////////////////////////////////////////////////
// MIT License
//
// Copyright (c) 2026 Colin Paice
// //
// Permission is hereby granted, free of charge, to any person
// obtaining a copy of this software and associated
// documentation files (the "Software"), to deal in the Software
// without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to
// whom the Software is furnished to do so, subject to the
// following conditions:
//
// The above copyright notice and this permission notice shall
// be included in all copies or substantial portions of the
// Software.
//
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
// KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
// WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
// PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
// COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
// SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//
// ================================================================

// Notes:
//  This program needs to be compiled as 64 bit and ascii for Python to support
//

#include <errno.h>           
#include <stdio.h> 
#include <unistd.h>          
#include <stdlib.h>  
#include <stddef.h>          
#include <string.h>          
#include <limits.h>          
#include <smfreal.h>         
#include <stdint.h>          
#include <printhex.h>        
#include <sys/time.h>  
#include <time.h>

////////////////////////////////////////////////////////////// 
//  mystrerror convert a reason code to a string 
////////////////////////////////////////////////////////////// 

char * mystrerror(int rc){
  // convert a return code to a reason string
  char * pText;
  
  switch (rc){
    case    0:      pText = "OK"; break; 
    case    0x00000c02: pText = "SMF not active"; break; 
    case    0x00000c03: pText = "Storage obtain error"; break; 
    case    0x00000401: pText = "Records skipped"; break; 
    case    0x00000402: pText = "In Mem removed"; break; 
    case    0x00000403: pText = "No data available"; break; 
    case    0x00000405: pText = "Get already in progress"; break; 
    case    0x00000406: pText = "Get when Disc in progress"; break; 
    case    0x00000407: pText = "Disconnect in progress"; break; 
    case    0x00000408: pText = "Get while disc in progress"; break; 
    case    0x00000801: pText = "Incorrect mode"; break; 
    case    0x00000802: pText = "Parmlist control block problems"; break; 
    case    0x00000803: pText = "No connection"; break; 
    case    0x00000804: pText = "Bad token"; break; 
    case    0x00000805: pText = "Unsupported operation"; break; 
    case    0x00000806: pText = "Buffer too small"; break; 
    case    0x00000807: pText = "No such resource"; break; 
    case    0x00000808: pText = "Query buffer too small "; break; 
    default: pText =  pText = "Internal Error"; break; 
     
  }
  return pText;
  
}

////////////////////////////////////////////////////////////// 
//  connect to the SMF resource  
//  parameters:
//      &SMF resource name null terminated string
//      & handle - 16 byte string
//       int debug 0 off, 1 on 2, more infor
//   returns reason  
////////////////////////////////////////////////////////////// 

int conn(const char* resource_name, char * pOut,int * debug) 
{ 
    char * pRName = (char *) resource_name; 
    //if (*debug  == 2) 
    //{ 
    //  if (__CHARSET_LIB  == 1) printf("Compiled as ASCII\n"); 
    //  else printf("Complied as not ASCII"); 
    //}
    // need EBCDIC constants 
    #pragma convert("IBM-1047") 
    char * pEye = "CNPB"; 

    #pragma convert(pop) 
    int lName = strlen(resource_name); 
    if  (*debug >= 1) 
    { 
      printf("===conn resource_name\n"); 
      printHex(stdout,pRName,20); 
    } 
    // SMFRealTime control block
    cnpb  hconn; 
    memset (pOut,0,16); // set the tokebn value to 0
    memset(&hconn,0,sizeof(hconn)); 
    memcpy(&hconn.CnPb_Eyecatcher,pEye,4); 
    hconn.CnPb_Length = sizeof(hconn);                                                                            
    hconn.CnPb_Version= 1;                                                                            
    if (lName  > sizeof (hconn.CnPb_Name)) 
    { 
      printf("Error Length of input name > 26 "); 
      printHex(stdout,pRName,32); 
      return 20; 
    } 
    hconn.CnPb_NameLength = lName; 
                                                                           
    memset(&hconn.CnPb_Name, 0x40, sizeof(hconn.CnPb_Name)); 
    strncpy(hconn.CnPb_Name, resource_name,   lName); 
                                                                           
    int retcode = 0;            /* Initial retcode prime */ 
    int rsncode = 0;            /* Initial rsncode prime */ 
    // printHex(stdout,&hconn,sizeof(hconn)); 
    IFAMCON(&hconn, &retcode, &rsncode); 
    if (retcode  != 0 && debug > 0) 
    { 
       printf("IFAMCON  rs %8.8x %s\n",rsncode,mystrerror(rsncode)); 
    } 
                                                                                    
                                                                                      
    memcpy(pOut,hconn.CnPb_Token,16); 
    if (*debug > 0) 
    { 
      printf("debug token after conn:"); 
      printHex(stdout,pOut,16); 
    }                                                                       
    return rsncode; 
} 


////////////////////////////////////////////////////////////// 
//  disconnect 
//  Parameters:
//  & handle
//  int debug  0 off, 1 or 2
////////////////////////////////////////////////////////////// 
 
int disc(char * pToken, int * debug) 
{ 
  // need ebcdic constants - program is compiled as ASCII
   #pragma convert("IBM-1047") 
   char * pEye = "DSPB"; 
   #pragma convert(pop) 
  
   dspb  hDisc; 
   memset(&hDisc,0,sizeof(hDisc)); 
   memcpy(&hDisc.DsPb_Eyecatcher,pEye,4); 
   hDisc.DsPb_Length = sizeof(hDisc); 
   hDisc.DsPb_Version= 1; 

   memcpy(&hDisc.DsPb_Token,pToken,sizeof(hDisc.DsPb_Token)); // Move token
                                                                           
                      
   int retcode = 0;           /* Initial retcode prime */ 
   int rsncode = 0;            /* Initial rsncode prime */ 
   if (* debug >= 2)
   {
     printHex(stdout,&hDisc,sizeof(hDisc));     
   }
   // printHex(stdout,&hconn,sizeof(hconn)); 
   IFAMDSC(&hDisc, &retcode, &rsncode); 
   if (retcode  != 0 && debug > 0) 
   { 
     printf("debug: IFAMDSC %8.8x %s\n",rsncode,mystrerror(rsncode)); 
   }                                                    
   return rsncode; 
} 
                                                                           
////////////////////////////////////////////////////////////// 
//  get 
//  Parameters:
//     & token
//     & output buffer
//     & length output buffer
//     char flag 
//     int debug 0, 1,2 
////////////////////////////////////////////////////////////// 

int get(char * pToken, char * pOut,int * lBuffer, char flag, int * debug) 
{           
    // need ebcdic constants.  Code is compiled as ASCII
    #pragma convert("IBM-1047")                                                    
    char * pEye = "GTPB";  // ebcdic eye catcher                                                           
    #pragma convert(pop) 

    gtpb   getBlock; 
    if ( * debug >=2 ) 
    { 
      printf("Input token\n");     
      printHex(stdout,pToken,16); 
      printf("Flag %2.2x\n",flag);    
    } 
    if (* debug > 0 )
      if (0x10 && flag == 0x10)
        printf(" Nowait flag is on\n");
      else 
        printf(" Wait flag is on\n");
    // set up the control blocks
    memset(&getBlock,0,sizeof(getBlock)); 
    memcpy(&getBlock.GtPb_Eyecatcher,pEye,4); 
    getBlock. GtPb_Length = sizeof(getBlock); 
    getBlock.GtPb_Version= 1; 
    memcpy(&getBlock.GtPb_Token,pToken,16); 
    getBlock.GtPb_BufferLength = * lBuffer; 
    getBlock.GtPb_BufferPtr = pOut; 
    getBlock.GtPb_Flags[0] = flag ; // no requests- 0x10 is do not block 
    int inLength = * lBuffer; 
    int retcode = 0;           /* Initial retcode prime */ 
    int rsncode = 0;            /* Initial rsncode prime */ 
    if ( * debug >= 2) 
    { 
      printf("Before get:Control block\n"); 
      printHex(stdout,&getBlock,sizeof(getBlock)); 
    } 
    // time the requests
    struct timeval loopStart, loopEnd ; 
    gettimeofday( &loopStart,0 ); 
                                                                                             
    IFAMGET(&getBlock, &retcode, &rsncode); 
    gettimeofday( &loopEnd,0 ); 
                                                                              
    // capture the duration of the get call - and when it happened
    if ( * debug > 0) 
    { 
       time_t temptime;
       struct tm *timeptr;
 
       timeptr = localtime(&loopEnd.tv_sec);
       char dateTime[21];
      // format as hh:mm:ss (no microseconds)
      strftime(&dateTime[0], sizeof(dateTime) - 1, "%H:%M:%S", timeptr);
      // print the formatted time and include the microseconds
      printf("Date Time %s.%6.6i\n", &dateTime,loopEnd.tv_usec);
      // calculate the duration in milliseconds
      //int duration = (loopEnd.tv_sec*1000.0 + loopEnd.tv_usec/1000.0 ) - 
      //   ( loopStart.tv_sec*1000.0 + loopStart.tv_usec/1000.0 ); 
      int duration = (loopEnd.tv_sec -loopStart.tv_sec)*1000.0 + 
                     (loopEnd.tv_usec - loopStart.tv_usec)/1000;
      printf("%s.%6.6i.  Get duration %i ms\n", &dateTime,loopEnd.tv_usec,duration);   
                                                                                                 
      printf("IFAMGET rs %4.4x %s\n", rsncode,mystrerror(rsncode)); 
      printf("Returned buffer length %i input length %i\n",getBlock.GtPb_ReturnedLength, 
        inLength); 
    } 
    // if it worked, pass back the length of data received
    if (retcode == 0 ) 
        * lBuffer = getBlock.GtPb_ReturnedLength; 
    else 
        * lBuffer = 0; 
    if (retcode == 0 && * debug > 1) 
    { 
      // print the data in hex                                                               
      int pLen = 2564; 
      if (*lBuffer < pLen) 
          pLen = * lBuffer; 
      printHex(stdout,pOut,pLen); 
    } 
    // print SMF record header information
    if (retcode == 0 && * debug > 0)
    {
       char type;
       char sysid[4];  //  subsystem name
       type = pOut[5]; //  SMF record type  
       short subtype; 
       int iType = type; // make integer out of it
       printf("SMF Header\n");
       printHex(stdout,pOut,16);
       // we need to convert from EBCDIC to ASCII so printf will display it 
       memcpy(&sysid,&pOut[14],4);
       __e2a_l(sysid,sizeof(sysid)); // convert in place 
       memcpy(&subtype,&pOut[22],2);
       int stype = subtype;  // make integer out of it
       printf("Type %i subtype %i subsystem %4.4s length %i\n",iType,stype, sysid,getBlock.GtPb_ReturnedLength);

    }

    return rsncode; 
}  

///////////////////////////////////////////////
//   query - display what SMF Real Time records are available
//   Parmeters:
//      debug 0,1,2 
////////////////////////////////////////////// 

int query(int * debug) {  

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
    typedef  struct result{                                                           
      uint16_t    lName;                                                              
      char        name[26];                                                           
      char        mask[32]; // length 32                                               
      uint32_t    reserved60 ;                                                        
      uint32_t    reserved64 ; /// cant use unit64_t because of alignment issue       
     } result;                                                                        
                                                                                      
    if ( sizeof(result) != 68)                                                        
    {                                                                                 
       printf("Internal error query size of result is wrong: %i\n",sizeof(result));                  
       return 8;                                                                      
    }                                                                                 
    extern int IFAMQRYN(querycb*, int *, int *);  /* Function definition */           
    #pragma linkage(IFAMQRY,OS64_NOSTACK)                                             
    
    // We need EBCDIC constants - program is compiled in ASCII
    #pragma convert("IBM-1047")                                                       
                                                                                     
    char * pEye = "QRPB";                                                             
                                                                                      
    #pragma convert(pop)                                                              
    char buffer[32768];                                                               
                                                                                      

    querycb myQuery;                                                             
                                                                                  
    memset(&myQuery,0,sizeof(myQuery));                                            
    memcpy(&myQuery.Eyecatcher,pEye,4);                                            
    myQuery.Length = sizeof(myQuery);                                              
    myQuery.Version = 1;                                                           
    myQuery.lBuffer = sizeof(buffer);                                              
    myQuery.pBuffer = &buffer[0];                                                  
    // #printf("Length query %i\n",sizeof(myQuery));                                   
    int retcode = 0;           /* Initial retcode prime */                         
    int rsncode = 0;            /* Initial rsncode prime */ 
    if ( * debug  > 1)
    {  
      printf("Before query\n");                                                      
      printHex(stdout,&myQuery,sizeof(myQuery));                                     
    }
    IFAMQRY(&myQuery, &retcode, &rsncode);                                         
    
    if ( * debug > 0 )
    {
      printf("IFAMQRY rs %8.8x %s\n",rsncode,mystrerror(rsncode));                              
      printf("Returned buffer count %i \n",myQuery.Count);                           
    }
                                                                        
    if ( myQuery.Count == 0)
    {
      printf("No records returned\n");
    }
    else
    {
        result * pResult = (struct result *)  &buffer;                                 
        int i; // each record                                                                      
        int b; // byte                                                                
        int j; // iterate over bits                                                   
        char c; 
        printf("Name                       Types\n");                      
        for (i=0;i< myQuery.Count;i++)                                              
        {    
          // convert from EBCDIC name to ASCII - so printf works when compiled as ASCII                                                                         
          int x =  __e2a_l(pResult->name,sizeof(pResult->name)); // convert in place 

          printf("%26.26s ",pResult->name);   
          // display the bits numbers which are on, showing the record types
          // loop for each byte flag
          //   look at the top bit 
          //   if on say so
          //   shift left 1 bit 
          for (b= 0;b<32;b++)  // 32 bytes                                                      
          {                                                                          
            c = pResult-> mask[b];                                                  
            for (j = 0;j<8;j++)                                                     
              {                                                                       
                if ((c & 0x80) == 0x80)                                   
                    printf("%i,",(8*b)+ j );                                                 
                                                              
                c = c<<1 ;//move it up 1                                             
              }                                                                      
          }                                                                          
          pResult += 1;                                                              
          printf("\n");                                                              
        } 
    }                                                                             
                                                              
  return rsncode;                                                                
}   

  