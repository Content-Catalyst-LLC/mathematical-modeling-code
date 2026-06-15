#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double f(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
double gx(double x, double y){ (void)x; return 3.0 + 0.5*y; }
double gy(double x, double y){ (void)y; return 2.0 + 0.5*x; }
void normalize(double vx, double vy, double *ux, double *uy){ double norm = sqrt(vx*vx + vy*vy); if(norm == 0.0){ fprintf(stderr, "Direction vector must be nonzero.\n"); exit(1); } *ux = vx/norm; *uy = vy/norm; }
double directional_derivative(double x, double y, double ux, double uy){ return gx(x,y)*ux + gy(x,y)*uy; }
int feasible_direction(double x, double y, double ux, double uy, double step){ return x >= 0.0 && y >= 0.0 && x+y <= 10.0 && x+step*ux >= 0.0 && y+step*uy >= 0.0 && x+step*ux+y+step*uy <= 10.0; }

int main(void){
  double cases[3][5] = {{4.0,3.0,1.0,1.0,0.25},{4.0,3.0,2.0,-1.0,0.25},{8.0,1.0,1.0,1.0,1.0}};
  printf("x,y,direction_x,direction_y,unit_x,unit_y,gradient_x,gradient_y,directional_derivative,step_size,estimated_change,actual_change,absolute_error,feasible_direction,warning\n");
  for(int i=0; i<3; i++){
    double x=cases[i][0], y=cases[i][1], vx=cases[i][2], vy=cases[i][3], step=cases[i][4];
    double ux, uy; normalize(vx, vy, &ux, &uy);
    double deriv = directional_derivative(x,y,ux,uy);
    double estimated = step * deriv;
    double actual = f(x+step*ux, y+step*uy) - f(x,y);
    int feasible = feasible_direction(x,y,ux,uy,step);
    printf("%.6f,%.6f,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.6f,%.12f,%.12f,%.12f,%d,%s\n", x,y,vx,vy,ux,uy,gx(x,y),gy(x,y),deriv,step,estimated,actual,fabs(actual-estimated),feasible, feasible ? "" : "Direction and step move outside the feasible region.");
  }
  return EXIT_SUCCESS;
}
