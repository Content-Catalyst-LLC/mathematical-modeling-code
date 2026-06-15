#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <utility>

constexpr double PI = 3.14159265358979323846;

std::pair<double,double> vector_field(double x, double y){ return {-y, x}; }
double dot2(std::pair<double,double> a, std::pair<double,double> b){ return a.first*b.first + a.second*b.second; }

void audit(double radius, int segments, const std::string& scenario){
  double flux_total = 0.0, circulation_total = 0.0, tangent_sum = 0.0, normal_sum = 0.0;
  for(int i=0; i<segments; i++){
    double theta0 = 2.0*PI*i/segments;
    double theta1 = 2.0*PI*(i+1)/segments;
    double x0 = radius*std::cos(theta0), y0 = radius*std::sin(theta0);
    double x1 = radius*std::cos(theta1), y1 = radius*std::sin(theta1);
    double xm = 0.5*(x0+x1), ym = 0.5*(y0+y1);
    double dx = x1-x0, dy = y1-y0;
    double segment_length = std::sqrt(dx*dx + dy*dy);
    auto tangent = std::make_pair(dx/segment_length, dy/segment_length);
    auto normal = std::make_pair(xm/radius, ym/radius);
    auto field = vector_field(xm, ym);
    circulation_total += dot2(field, std::make_pair(dx,dy));
    flux_total += dot2(field, normal) * segment_length;
    tangent_sum += dot2(field, tangent);
    normal_sum += dot2(field, normal);
  }
  std::string warning = segments < 32 ? "Coarse path sampling; circulation and flux should be checked with more segments." : "Synthetic flow audit; document field meaning orientation units and boundary choice.";
  std::cout << scenario << "," << segments << "," << flux_total << "," << circulation_total << "," << tangent_sum/segments << "," << normal_sum/segments << ",rotating field F=<-y,x>,counterclockwise circle with radius 1," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,segment_count,approximate_flux,approximate_circulation,mean_tangential_alignment,mean_normal_alignment,field_description,geometry_description,warning\n";
  audit(1.0, 16, "coarse_circle");
  audit(1.0, 64, "medium_circle");
  audit(1.0, 256, "fine_circle");
}
