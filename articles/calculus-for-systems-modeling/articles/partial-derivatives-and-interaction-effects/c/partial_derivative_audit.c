#include <stdio.h>
#include <stdlib.h>

double system_response(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
double partial_x(double x, double y){ (void)x; return 3.0 + 0.5*y; }
double partial_y(double x, double y){ (void)y; return 2.0 + 0.5*x; }
double cross_partial_xy(double x, double y){ (void)x; (void)y; return 0.5; }
int is_feasible(double x, double y){ return x >= 0.0 && y >= 0.0 && x + y <= 10.0; }

int main(void){
  double cases[3][2] = {{2.0,4.0},{8.0,4.0},{6.0,3.0}};
  printf("x,y,output,partial_x,partial_y,cross_partial_xy,feasible,warning\n");
  for(int i=0; i<3; i++){
    double x = cases[i][0], y = cases[i][1];
    int feasible = is_feasible(x,y);
    printf("%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%d,%s\n", x, y, system_response(x,y), partial_x(x,y), partial_y(x,y), cross_partial_xy(x,y), feasible, feasible ? "" : "Input combination is outside the feasible region.");
  }
  return EXIT_SUCCESS;
}
