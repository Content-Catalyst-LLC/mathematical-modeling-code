#include <cmath>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>

double f(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
double gx(double, double y){ return 3.0 + 0.5*y; }
double gy(double x, double){ return 2.0 + 0.5*x; }
std::pair<double,double> normalize(double vx, double vy){ double norm = std::sqrt(vx*vx + vy*vy); if(norm == 0.0) throw std::runtime_error("Direction vector must be nonzero."); return {vx/norm, vy/norm}; }
double directional_derivative(double x, double y, double ux, double uy){ return gx(x,y)*ux + gy(x,y)*uy; }
bool feasible_direction(double x, double y, double ux, double uy, double step){ return x >= 0.0 && y >= 0.0 && x+y <= 10.0 && x+step*ux >= 0.0 && y+step*uy >= 0.0 && x+step*ux+y+step*uy <= 10.0; }

int main(){
  std::vector<std::vector<double>> cases = {{4.0,3.0,1.0,1.0,0.25},{4.0,3.0,2.0,-1.0,0.25},{8.0,1.0,1.0,1.0,1.0}};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "x,y,direction_x,direction_y,unit_x,unit_y,gradient_x,gradient_y,directional_derivative,step_size,estimated_change,actual_change,absolute_error,feasible_direction,warning\n";
  for(auto row : cases){
    double x=row[0], y=row[1], vx=row[2], vy=row[3], step=row[4];
    auto unit = normalize(vx,vy);
    double ux=unit.first, uy=unit.second;
    double deriv=directional_derivative(x,y,ux,uy);
    double estimated=step*deriv;
    double actual=f(x+step*ux,y+step*uy)-f(x,y);
    bool feasible=feasible_direction(x,y,ux,uy,step);
    std::cout << x << "," << y << "," << vx << "," << vy << "," << ux << "," << uy << "," << gx(x,y) << "," << gy(x,y) << "," << deriv << "," << step << "," << estimated << "," << actual << "," << std::abs(actual-estimated) << "," << feasible << "," << (feasible ? "" : "Direction and step move outside the feasible region.") << "\n";
  }
}
