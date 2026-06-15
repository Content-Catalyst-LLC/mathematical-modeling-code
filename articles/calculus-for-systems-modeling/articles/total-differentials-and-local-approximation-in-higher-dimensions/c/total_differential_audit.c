#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double f(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
double fx(double x, double y){ (void)x; return 3.0 + 0.5*y; }
double fy(double x, double y){ (void)y; return 2.0 + 0.5*x; }
double total_differential(double x, double y, double dx, double dy){ return fx(x,y)*dx + fy(x,y)*dy; }
int feasible_displacement(double x, double y, double dx, double dy){ return x >= 0.0 && y >= 0.0 && x + y <= 10.0 && x + dx >= 0.0 && y + dy >= 0.0 && x + dx + y + dy <= 10.0; }

int main(void){
  double cases[3][4] = {{4.0,3.0,0.2,-0.1},{4.0,3.0,1.0,1.0},{8.0,1.0,1.0,1.0}};
  printf("x,y,dx,dy,baseline_output,actual_output,actual_change,differential_estimate,absolute_error,feasible_displacement,warning\n");
  for(int i=0; i<3; i++){
    double x = cases[i][0], y = cases[i][1], dx = cases[i][2], dy = cases[i][3];
    double baseline = f(x,y);
    double actual = f(x+dx,y+dy);
    double change = actual - baseline;
    double estimate = total_differential(x,y,dx,dy);
    int feasible = feasible_displacement(x,y,dx,dy);
    printf("%.6f,%.6f,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%d,%s\n", x, y, dx, dy, baseline, actual, change, estimate, fabs(change-estimate), feasible, feasible ? "" : "Displacement is outside the feasible region.");
  }
  return EXIT_SUCCESS;
}
