#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void rates(double prey, double predator, double alpha, double beta, double delta, double gamma, double* prey_rate, double* predator_rate){
  *prey_rate = alpha*prey - beta*prey*predator;
  *predator_rate = delta*prey*predator - gamma*predator;
}

int main(void){
  double prey = 40.0, predator = 9.0, alpha = 0.7, beta = 0.05, delta = 0.02, gamma = 0.5, dt = 0.01;
  int steps = 2000;
  printf("scenario,time,prey,predator,prey_rate,predator_rate,alpha,beta,delta,gamma,method,warning\n");
  for(int n=0; n<=steps; n++){
    double t = n*dt;
    double prey_rate, predator_rate;
    rates(prey, predator, alpha, beta, delta, gamma, &prey_rate, &predator_rate);
    printf("predator_prey_coupled_system,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,explicit_euler,Predator-prey terms are illustrative and assume continuous well-mixed interaction.\n",
      t, prey, predator, prey_rate, predator_rate, alpha, beta, delta, gamma);
    prey = fmax(0.0, prey + dt*prey_rate);
    predator = fmax(0.0, predator + dt*predator_rate);
  }
  return EXIT_SUCCESS;
}
