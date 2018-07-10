SET_DEC_FILE "PIN.dec" 

HEADER P04,P10,P12,P11;         

SPM_PATTERN (Flash_Unlock) {             
                           
                *0 00X*TS1;         
                *0 00X*RPT 1000;          
                *0 11X*;//Cmd_0XAA
                *0 10X*;
                *0 11X*;
                *0 10X*;
                *0 11X*;
                *0 10X*;
                *0 11X*;
                *0 10X*;
                *0 10X*;//Cmd_0X70
                *0 11X*;
                *0 11X*;
                *0 11X*;
                *0 10X*;
                *0 10X*;
                *0 10X*;
                *0 10X*;
                *0 00X*RPT 2;              
                *0 10L*;//Cmd_0X1A
                *0 10X*;
                *0 10X*;
                *0 11X*;
                *0 11X*;
                *0 10X*;
                *0 11X*;
                *0 10X*;
                *0 00X*RPT 2;
                *0 00H*;
              
                *0 00X*STOP;
}
