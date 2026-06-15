#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <utility>

constexpr double PI = 3.14159265358979323846;

std::pair<double,double> path_point(double t){ return {t, std::sin(t)}; }
double scalar_field(double x, double y){ (void)x; return 1.0 + y*y; }
std::pair<double,double> vector_field(double x, double y){ (void)y; return {1.0, x}; }
double distance_between(std::pair<double,double> p, std::pair<double,double> q){ return std::sqrt((q.first-p.first)*(q.first-p.first)+(q.second-p.second)*(q.second-p.second)); }
double dot(std::pair<double,double> a, std::pair<double,double> b){ return a.first*b.first + a.second*b.second; }

void audit(double step, const std::string& scenario){
  int count = static_cast<int>((2.0*PI)/step) + 1;
  double path_len = 0.0, scalar_total = 0.0, vector_total = 0.0, align_sum = 0.0, max_seg = 0.0;
  for(int i=0; i<count-1; i++){
    double t = i * step;
    auto p = path_point(t);
    auto q = path_point(t+step);
    auto disp = std::make_pair(q.first-p.first, q.second-p.second);
    double seg = distance_between(p,q);
    auto field = vector_field(p.first,p.second);
    double term = dot(field, disp);
    path_len += seg;
    scalar_total += scalar_field(p.first,p.second) * seg;
    vector_total += term;
    align_sum += term / std::max(seg, 1e-12);
    max_seg = std::max(max_seg, seg);
  }
  std::string warning = step > 0.5 ? "Time step is coarse; path turns and field variation may be undersampled." : "Synthetic line-integral audit; document path field units and interpolation.";
  std::cout << scenario << "," << step << "," << count << "," << path_len << "," << scalar_total << "," << vector_total << "," << align_sum/(count-1) << "," << max_seg << ",path r(t)=<t,sin(t)>," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,time_step,point_count,path_length,scalar_line_integral,vector_line_integral,average_alignment,maximum_segment_length,path_description,warning\n";
  audit(1.0, "coarse_path");
  audit(0.5, "medium_path");
  audit(0.25, "fine_path");
}
