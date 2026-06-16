#include <cmath>
#include <iostream>
double exponential(double n0,double r,double t){ return n0*std::exp(r*t); }
double logistic(double n0,double r,double k,double t){ return k/(1.0+((k-n0)/n0)*std::exp(-r*t)); }
int main(){ double n0=100,r=.08,k=1000; std::cout<<"time,exponential,logistic\n"; for(int t=0;t<=40;t+=5) std::cout<<t<<","<<exponential(n0,r,t)<<","<<logistic(n0,r,k,t)<<"\n"; }
