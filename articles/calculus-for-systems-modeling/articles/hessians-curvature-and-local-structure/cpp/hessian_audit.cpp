#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double f_model(double x, double y){ return x*x + x*y + 3.0*y*y + 0.2*x*x*y; }
std::pair<double,double> gradient(double x, double y){ return {2.0*x + y + 0.4*x*y, x + 6.0*y + 0.2*x*x}; }
std::string classify(double h11, double h12, double h21, double h22){
  double det = h11*h22 - h12*h21;
  if(det > 0.0 && h11 > 0.0) return "positive definite";
  if(det > 0.0 && h11 < 0.0) return "negative definite";
  if(det < 0.0) return "indefinite";
  return "semidefinite or inconclusive";
}

int main(){
  std::vector<std::vector<double>> cases = {{2.0,1.0,0.1,-0.05},{2.0,1.0,0.5,0.5},{-5.0,0.0,0.2,0.1}};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "x,y,dx,dy,gradient_x,gradient_y,h11,h12,h21,h22,determinant,trace,classification,first_order_change,second_order_change,actual_change,first_order_error,second_order_error,warning\n";
  for(auto row : cases){
    double x=row[0], y=row[1], dx=row[2], dy=row[3];
    auto g=gradient(x,y);
    double h11=2.0+0.4*y, h12=1.0+0.4*x, h21=h12, h22=6.0;
    double det=h11*h22-h12*h21;
    std::string cl=classify(h11,h12,h21,h22);
    double first=g.first*dx+g.second*dy;
    double second=first+0.5*(h11*dx*dx+2.0*h12*dx*dy+h22*dy*dy);
    double actual=f_model(x+dx,y+dy)-f_model(x,y);
    std::string warning = det < 0.0 ? "Hessian is indefinite; local structure is saddle-like." : (std::abs(det)<1e-8 ? "Hessian is singular or nearly singular." : "");
    std::cout << x << "," << y << "," << dx << "," << dy << "," << g.first << "," << g.second << "," << h11 << "," << h12 << "," << h21 << "," << h22 << "," << det << "," << h11+h22 << "," << cl << "," << first << "," << second << "," << actual << "," << std::abs(actual-first) << "," << std::abs(actual-second) << "," << warning << "\n";
  }
}
