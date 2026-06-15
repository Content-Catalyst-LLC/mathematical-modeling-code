#include <stdio.h>
#include <stdlib.h>
double system_response(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
int is_feasible(double x, double y){ return x >= 0.0 && y >= 0.0 && x + y <= 10.0; }
int main(void){
  double cases[3][2] = {{2.0,4.0},{8.0,4.0},{6.0,3.0}};
  printf("x,y,output,feasible,warning\n");
  for(int i=0; i<3; i++){
    double x = cases[i][0], y = cases[i][1];
    int feasible = is_feasible(x,y);
    printf("%.6f,%.6f,%.12f,%d,%s\n", x, y, system_response(x,y), feasible, feasible ? "" : "Input combination is outside the feasible region.");
  }
  return EXIT_SUCCESS;
}
