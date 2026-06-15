#include <iomanip>
#include <iostream>

double logistic_rate(double x, double growth, double carrying){ return growth*x*(1.0 - x/carrying); }
double bistable_rate(double x, double threshold){ return x*(1.0-x)*(x-threshold); }

int main(){
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "scenario,time,state,rate,parameter_a,parameter_b,parameter_c,method,warning\n";
  double x = 10.0, dt = 0.05, growth = 0.6, carrying = 100.0;
  for(int n=0; n<=300; n++){
    double t = n*dt;
    double r = logistic_rate(x, growth, carrying);
    std::cout << "logistic_growth," << t << "," << x << "," << r << "," << growth << "," << carrying << ",0.000000,explicit_euler,Logistic growth assumes a fixed carrying capacity and smooth density limitation.\n";
    x = x + dt*r;
  }
  x = 0.35;
  double threshold = 0.4;
  for(int n=0; n<=300; n++){
    double t = n*dt;
    double r = bistable_rate(x, threshold);
    std::cout << "bistable_threshold," << t << "," << x << "," << r << "," << threshold << ",0.000000,0.000000,explicit_euler,Threshold behavior is illustrative and should not be interpreted without evidence for the threshold.\n";
    x = x + dt*r;
  }
}
