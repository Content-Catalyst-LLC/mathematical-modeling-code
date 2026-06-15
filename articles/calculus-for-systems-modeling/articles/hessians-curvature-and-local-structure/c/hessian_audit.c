#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double f_model(double x, double y){ return x*x + x*y + 3.0*y*y + 0.2*x*x*y; }
void gradient(double x, double y, double *gx, double *gy){ *gx = 2.0*x + y + 0.4*x*y; *gy = x + 6.0*y + 0.2*x*x; }
void hessian(double x, double y, double *h11, double *h12, double *h21, double *h22){ *h11 = 2.0 + 0.4*y; *h12 = 1.0 + 0.4*x; *h21 = 1.0 + 0.4*x; *h22 = 6.0; }

const char* classify(double h11, double h12, double h21, double h22){
  double det = h11*h22 - h12*h21;
  if(det > 0.0 && h11 > 0.0) return "positive definite";
  if(det > 0.0 && h11 < 0.0) return "negative definite";
  if(det < 0.0) return "indefinite";
  return "semidefinite or inconclusive";
}

int main(void){
  double cases[3][4] = {{2.0,1.0,0.1,-0.05},{2.0,1.0,0.5,0.5},{-5.0,0.0,0.2,0.1}};
  printf("x,y,dx,dy,gradient_x,gradient_y,h11,h12,h21,h22,determinant,trace,classification,first_order_change,second_order_change,actual_change,first_order_error,second_order_error,warning\n");
  for(int i=0; i<3; i++){
    double x=cases[i][0], y=cases[i][1], dx=cases[i][2], dy=cases[i][3];
    double gx,gy,h11,h12,h21,h22; gradient(x,y,&gx,&gy); hessian(x,y,&h11,&h12,&h21,&h22);
    double det=h11*h22-h12*h21;
    const char* cl=classify(h11,h12,h21,h22);
    double first=gx*dx+gy*dy;
    double quad=0.5*(h11*dx*dx+2.0*h12*dx*dy+h22*dy*dy);
    double second=first+quad;
    double actual=f_model(x+dx,y+dy)-f_model(x,y);
    const char* warning=(det < 0.0) ? "Hessian is indefinite; local structure is saddle-like." : (fabs(det)<1e-8 ? "Hessian is singular or nearly singular." : "");
    printf("%.6f,%.6f,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%.12f,%.12f,%.12f,%.12f,%.12f,%s\n", x,y,dx,dy,gx,gy,h11,h12,h21,h22,det,h11+h22,cl,first,second,actual,fabs(actual-first),fabs(actual-second),warning);
  }
  return EXIT_SUCCESS;
}
