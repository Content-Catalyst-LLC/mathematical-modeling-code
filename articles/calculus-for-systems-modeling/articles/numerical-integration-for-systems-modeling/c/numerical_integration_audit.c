#include <math.h>
#include <stdio.h>
double rate(double t){ return 2.0 + sin(t) + 0.1*t; }
double trueint(double t){ return 2.0*t - cos(t) + 1.0 + 0.05*t*t; }
int main(){ double h=0.1,left=0,trap=0; printf("index,time,rate,left_cumulative,trapezoid_cumulative,true_cumulative,error\n"); for(int i=0;i<=100;i++){ double t=i*h,r=rate(t); if(i>0){ left+=rate((i-1)*h)*h; trap+=0.5*(rate((i-1)*h)+r)*h; } double truth=trueint(t)-trueint(0); printf("%d,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n",i,t,r,left,trap,truth,fabs(trap-truth)); } return 0; }
