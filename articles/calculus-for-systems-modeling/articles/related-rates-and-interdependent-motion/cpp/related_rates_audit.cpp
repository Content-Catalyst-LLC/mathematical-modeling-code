#include <iomanip>
#include <iostream>
#include <vector>

double volume(double h){ return 12.0*h*h; }
double d_volume_d_height(double h){ return 24.0*h; }
double height_path(double t){ return 2.0 + 0.08*t; }
double height_rate(double){ return 0.08; }

int main(){
  std::vector<double> ts={0.0,5.0,10.0,20.0,40.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"time,height,height_rate,volume,structural_derivative,inferred_volume_rate\n";
  for(double t:ts){
    double h=height_path(t), hr=height_rate(t), v=volume(h), structural=d_volume_d_height(h), inferred=structural*hr;
    std::cout<<t<<","<<h<<","<<hr<<","<<v<<","<<structural<<","<<inferred<<"\n";
  }
}
