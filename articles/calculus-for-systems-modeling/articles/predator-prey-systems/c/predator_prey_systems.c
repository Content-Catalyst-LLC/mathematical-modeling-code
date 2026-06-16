#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void){
  double alpha=0.6, beta=0.02, gamma=0.5, delta=0.01;
  double x=40.0, y=9.0, dt=0.02;
  int steps=4000;
  for(int i=0;i<steps;i++){
    double dx = alpha*x - beta*x*y;
    double dy = delta*x*y - gamma*y;
    x = fmax(0.0, x + dt*dx);
    y = fmax(0.0, y + dt*dy);
  }
  printf("scenario_name,model_type,final_prey,final_predator,warning\n");
  printf("classic_lotka_volterra,lotka_volterra,%.6f,%.6f,mass_action_baseline\n", x, y);
  return EXIT_SUCCESS;
}
