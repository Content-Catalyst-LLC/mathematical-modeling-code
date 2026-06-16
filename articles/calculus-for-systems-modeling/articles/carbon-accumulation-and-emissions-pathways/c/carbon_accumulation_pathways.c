#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double linear_decline(double e0, int year, int years){
  double v = e0 * (1.0 - ((double)year / (double)years));
  return v > 0.0 ? v : 0.0;
}

int main(void){
  double e0=40.0;
  int years=30;
  double cumulative=0.0;
  for(int y=0;y<=years;y++) cumulative += linear_decline(e0, y, years);
  printf("scenario_name,pathway_type,cumulative_emissions,warning\n");
  printf("linear_decline_to_zero,linear_decline,%.6f,linear_decline_still_accumulates_until_net_zero\n", cumulative);
  return EXIT_SUCCESS;
}
