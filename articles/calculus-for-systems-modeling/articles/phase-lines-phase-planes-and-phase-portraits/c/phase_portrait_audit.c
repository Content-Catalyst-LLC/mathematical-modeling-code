#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void rates(double x, double y, double alpha, double beta, double delta, double gamma, double* dxdt, double* dydt){
  *dxdt = alpha*x - beta*x*y;
  *dydt = delta*x*y - gamma*y;
}

int main(void){
  double alpha = 0.7, beta = 0.05, delta = 0.02, gamma = 0.5;
  printf("x,y,dxdt,dydt,x_nullcline_residual,y_nullcline_residual,speed,warning\n");
  for(int xi=0; xi<=60; xi+=5){
    for(int yi=0; yi<=30; yi+=3){
      double x = (double)xi;
      double y = (double)yi;
      double dxdt, dydt;
      rates(x, y, alpha, beta, delta, gamma, &dxdt, &dydt);
      double speed = sqrt(dxdt*dxdt + dydt*dydt);
      printf("%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Vector-field values depend on parameter values state ranges and the assumed interaction structure.\n", x, y, dxdt, dydt, dxdt, dydt, speed);
    }
  }
  return EXIT_SUCCESS;
}
