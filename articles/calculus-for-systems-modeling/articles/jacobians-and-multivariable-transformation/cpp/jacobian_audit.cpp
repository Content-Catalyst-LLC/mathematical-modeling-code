#include <cmath>
#include <iomanip>
#include <iostream>
#include <utility>
#include <vector>

std::pair<double,double> F_model(double x, double y){ return {x*x + y, x*y + 3.0*y}; }

int main(){
  std::vector<std::vector<double>> cases = {{2.0,1.0,0.1,-0.05},{2.0,1.0,0.5,0.5},{0.0,0.0,0.1,0.1}};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "x,y,dx,dy,j11,j12,j21,j22,determinant,approximate_change_1,approximate_change_2,actual_change_1,actual_change_2,error_norm,warning\n";
  for(auto row : cases){
    double x=row[0], y=row[1], dx=row[2], dy=row[3];
    double j11=2.0*x, j12=1.0, j21=y, j22=x+3.0;
    auto baseline=F_model(x,y); auto actual=F_model(x+dx,y+dy);
    double ac1=j11*dx+j12*dy, ac2=j21*dx+j22*dy;
    double rc1=actual.first-baseline.first, rc2=actual.second-baseline.second;
    double det=j11*j22-j12*j21;
    double err=std::sqrt((rc1-ac1)*(rc1-ac1)+(rc2-ac2)*(rc2-ac2));
    std::cout << x << "," << y << "," << dx << "," << dy << "," << j11 << "," << j12 << "," << j21 << "," << j22 << "," << det << "," << ac1 << "," << ac2 << "," << rc1 << "," << rc2 << "," << err << "," << (std::abs(det)>1e-8 ? "" : "Jacobian is singular or near singular.") << "\n";
  }
}
