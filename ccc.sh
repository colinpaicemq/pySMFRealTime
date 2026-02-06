name=pySMFRT
export STEPLIB="CBC.SCCNCMP"
export prefix_CLIB_PREFIX="CBC"
export _C89_CCMODE=1
export _C99_CCMODE=1
export _Ccc_CCMODE=1
export _CC_CCMODE=1
export _CXX_CCMODE=1
export _C89_CCMODE=1
export _CC_EXTRA_ARGS=1
export _CXX_EXTRA_ARGS=1
export _C89_EXTRA_ARGS=1
p1="-Wc,arch(8),target(zOSV2R3),list,source,lp64,gonum,asm,float(ieee)"
p2="-Wc,DLL -D_XOPEN_SOURCE_EXTENDED -D_POSIX_THREADS"
p3="            -qascii "
p3="-qexportall -qascii "
p5="                           -I.                            "
p6=""
p7="-Wc,ASM,ASMLIB(//'SYS1.MACLIB') "
p8="-Wc,LIST(c.lst),SOURCE,NOWARN64 -Wa,LIST,RENT"
xlc  $p1 $p2 $p3     $p5     $p7 $p8          -c $name.c -o $name.o

l1="-Wl,LIST,MAP,DLL,XREF  -q64"
/bin/xlc $name.o  -o pySMFRealTime.so            $l1    1>bind.lst
chtag -b pySMFRealTime.so
chtag -b pySMFRealTime.x
rm   $name.o
