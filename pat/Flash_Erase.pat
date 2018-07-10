SET_DEC_FILE "PIN.dec" 

HEADER P04,P10,P12,P11;         

SPM_PATTERN (Flash_Erase) {
ST:             *0 00X*TS1;         
                *0 11X*;//Cmd_0XAA
                *0 10X*;
                *0 11X*;
                *0 10X*;
                *0 11X*;
                *0 10X*;
                *0 11X*;
                *0 10X*;
                *0 10X*;//Cmd_0X71
                *0 11X*;
                *0 11X*;
                *0 11X*;
                *0 10X*;
                *0 10X*;
                *0 10X*;
                *0 11X*;
                *0 10X*;//Cmd_0X1B
                *0 10X*;
                *0 10X*;
                *0 11X*;
                *0 11X*;
                *0 10X*;
                *0 11X*;
                *0 11L*;
                *0 00X*TS5,RPT 15;
                *0 00H*TS1;
                *0 00X*STOP;
}
