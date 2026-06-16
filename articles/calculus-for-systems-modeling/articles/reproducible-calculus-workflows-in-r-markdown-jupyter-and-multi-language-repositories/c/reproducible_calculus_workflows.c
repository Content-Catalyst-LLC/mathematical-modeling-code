#include <stdio.h>
#include <stdlib.h>

int main(void){
  printf("artifact_name,artifact_type,path,source_or_generated,review_role,warning\n");
  printf("parameter_records,csv,data/parameter_records.csv,source,documents parameter names values units sources and ranges,Parameter records do not prove empirical correctness.\n");
  printf("model_outputs,csv,outputs/tables/model_outputs.csv,generated,stores computed trajectory or summary outputs,Generated outputs require diagnostics and interpretation limits.\n");
  printf("diagnostics,json,outputs/json/diagnostics.json,generated,records validation convergence and warning status,Diagnostics should remain attached to interpretation.\n");
  printf("governance_queue,markdown,outputs/reports/governance_queue.md,generated,collects warnings requiring human review,Governance queues support judgment but do not replace it.\n");
  return EXIT_SUCCESS;
}
