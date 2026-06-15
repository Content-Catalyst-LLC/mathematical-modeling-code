#include <stdio.h>
#include <stdlib.h>

double net_flow(double t){ return (12.0 + 0.5*t) - (7.0 + 0.2*t); }

int main(void){
  double stock = 100.0;
  double times[] = {0,1,2,3,4,5,6};
  printf("time,net_flow,recovered_stock,method\n");
  printf("%.6f,%.12f,%.12f,initial condition\n", times[0], net_flow(times[0]), stock);
  for(int i=1;i<7;i++){
    double previous = times[i-1];
    double current = times[i];
    double dt = current - previous;
    double area = 0.5 * (net_flow(previous) + net_flow(current)) * dt;
    stock += area;
    printf("%.6f,%.12f,%.12f,trapezoidal accumulation\n", current, net_flow(current), stock);
  }
  return EXIT_SUCCESS;
}
