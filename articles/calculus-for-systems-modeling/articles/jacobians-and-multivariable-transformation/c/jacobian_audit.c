#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void F_model(double x, double y, double *o1, double *o2){ *o1 = x*x + y; *o2 = x*y + 3.0*y; }
void jacobian(double x, double y, double *j11, double *j12, double *j21, double *j22){ *j11 = 2.0*x; *j12 = 1.0; *j21 = y; *j22 = x + 3.0; }

int main(void){
  double cases[3][4] = {{2.0,1.0,0.1,-0.05},{2.0,1.0,0.5,0.5},{0.0,0.0,0.1,0.1}};
  printf("x,y,dx,dy,j11,j12,j21,j22,determinant,approximate_change_1,approximate_change_2,actual_change_1,actual_change_2,error_norm,warning\n");
  for(int i=0; i<3; i++){
    double x=cases[i][0], y=cases[i][1], dx=cases[i][2], dy=cases[i][3];
    double j11,j12,j21,j22; jacobian(x,y,&j11,&j12,&j21,&j22);
    double b1,b2,a1,a2; F_model(x,y,&b1,&b2); F_model(x+dx,y+dy,&a1,&a2);
    double ac1=j11*dx+j12*dy, ac2=j21*dx+j22*dy;
    double rc1=a1-b1, rc2=a2-b2;
    double det=j11*j22-j12*j21;
    double err=sqrt((rc1-ac1)*(rc1-ac1)+(rc2-ac2)*(rc2-ac2));
    printf("%.6f,%.6f,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s\n", x,y,dx,dy,j11,j12,j21,j22,det,ac1,ac2,rc1,rc2,err, fabs(det)>1e-8 ? "" : "Jacobian is singular or near singular.");
  }
  return EXIT_SUCCESS;
}
