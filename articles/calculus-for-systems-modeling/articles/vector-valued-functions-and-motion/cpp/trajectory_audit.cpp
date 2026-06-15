#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <utility>

constexpr double PI = 3.14159265358979323846;

std::pair<double,double> position(double t){ return {t, std::sin(t)}; }
double distance_between(std::pair<double,double> p, std::pair<double,double> q){
  return std::sqrt((q.first-p.first)*(q.first-p.first)+(q.second-p.second)*(q.second-p.second));
}

void audit(double step, const std::string& scenario){
  int count = static_cast<int>((2.0*PI)/step) + 1;
  auto first = position(0.0);
  auto prev = first;
  double arc = 0.0, speed_sum = 0.0, speed_max = 0.0;
  for(int i=1; i<count; i++){
    double t = i * step;
    auto p = position(t);
    double seg = distance_between(prev, p);
    double speed = seg / step;
    arc += seg;
    speed_sum += speed;
    speed_max = std::max(speed_max, speed);
    prev = p;
  }
  double disp = distance_between(first, prev);
  double eff = disp / std::max(arc, 1e-12);
  std::string warning = step > 0.5 ? "Time step is coarse; turns and speed variation may be undersampled." : "Synthetic trajectory audit; document units parameter meaning and sampling.";
  std::cout << scenario << "," << step << "," << count << "," << arc << "," << disp << "," << eff << "," << speed_sum/(count-1) << "," << speed_max << ",trajectory r(t)=<t,sin(t)>," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,time_step,point_count,approximate_arc_length,displacement_magnitude,path_efficiency,average_speed,maximum_speed,domain_description,warning\n";
  audit(1.0, "coarse_time_step");
  audit(0.5, "medium_time_step");
  audit(0.25, "fine_time_step");
}
