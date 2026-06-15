#include <math.h>
#include <stdio.h>
#include <stdlib.h>

const char* classify(double d){
  if(d < -1e-8) return "locally_stable";
  if(d > 1e-8) return "locally_unstable";
  return "inconclusive_at_critical_value";
}

int main(void){
  printf("model,parameter_mu,equilibrium,derivative_value,stability,branch_status,warning\n");
  for(int step=-20; step<=40; step++){
    double mu = step / 10.0;
    if(mu < 0.0){
      printf("saddle_node_normal_form,%.6f,,,no_real_equilibrium,equilibrium_absent,For mu below zero the saddle-node normal form has no real equilibrium.\n", mu);
    } else if(fabs(mu) < 1e-12){
      double eq = 0.0;
      double d = -2.0 * eq;
      printf("saddle_node_normal_form,%.6f,%.6f,%.6f,%s,critical_branch,Bifurcation interpretation depends on model form parameter meaning and domain validity.\n", mu, eq, d, classify(d));
    } else {
      double root = sqrt(mu);
      double eqs[2] = {-root, root};
      for(int i=0; i<2; i++){
        double eq = eqs[i];
        double d = -2.0 * eq;
        printf("saddle_node_normal_form,%.6f,%.6f,%.6f,%s,equilibrium_present,Bifurcation interpretation depends on model form parameter meaning and domain validity.\n", mu, eq, d, classify(d));
      }
    }
  }
  return EXIT_SUCCESS;
}
