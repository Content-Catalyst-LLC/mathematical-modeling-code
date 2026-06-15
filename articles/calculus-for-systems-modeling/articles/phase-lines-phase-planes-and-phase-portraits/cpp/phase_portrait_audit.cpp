#include <cmath>
#include <iomanip>
#include <iostream>
#include <utility>

std::pair<double,double> rates(double x, double y, double alpha, double beta, double delta, double gamma){
  return {alpha*x - beta*x*y, delta*x*y - gamma*y};
}

int main(){
  double alpha = 0.7, beta = 0.05, delta = 0.02, gamma = 0.5;
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "x,y,dxdt,dydt,x_nullcline_residual,y_nullcline_residual,speed,warning\n";
  for(int xi=0; xi<=60; xi+=5){
    for(int yi=0; yi<=30; yi+=3){
      double x = static_cast<double>(xi);
      double y = static_cast<double>(yi);
      auto [dxdt, dydt] = rates(x, y, alpha, beta, delta, gamma);
      double speed = std::sqrt(dxdt*dxdt + dydt*dydt);
      std::cout << x << "," << y << "," << dxdt << "," << dydt << "," << dxdt << "," << dydt << "," << speed << ",Vector-field values depend on parameter values state ranges and the assumed interaction structure.\n";
    }
  }
}
