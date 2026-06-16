#include <stdio.h>
#include <stdlib.h>

int main(void){
  printf("record_type,name,role_or_process,evidence_or_requirement,status,warning\n");
  printf("mechanism_record,stock_flow_accumulation,stock changes through inflow and outflow,synthetic teaching example,review,flows must represent real processes\n");
  printf("mechanism_record,balancing_feedback,state-dependent adjustment limits growth,formal teaching example,review,feedback parameters require evidence\n");
  printf("formal_record,differential_equation,dxdt=f,process interpretation required,review,rate equation needs mechanism meaning\n");
  printf("claim_record,mechanistic,organized process produces behavior,process evidence required,review,scope depends on assumptions\n");
  printf("claim_record,exploratory,investigates possible behavior,scenario assumptions required,active,not a confirmed mechanism or forecast\n");
  return EXIT_SUCCESS;
}
