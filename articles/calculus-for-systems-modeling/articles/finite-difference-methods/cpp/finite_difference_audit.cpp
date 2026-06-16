#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
int main(){ int n=61, steps=120; double dx=1.0, dt=0.2, ratio=0.08*0.2; std::vector<double> field(n,0.0); field[n/2]=1.0; std::cout<<"step,time,center_value,total_mass,max_value,left_boundary,right_boundary,diffusion_ratio\n"; for(int s=0;s<=steps;s++){ double total=std::accumulate(field.begin(), field.end(), 0.0)*dx; double maxv=*std::max_element(field.begin(), field.end()); std::cout<<s<<","<<s*dt<<","<<field[n/2]<<","<<total<<","<<maxv<<","<<field.front()<<","<<field.back()<<","<<ratio<<"\n"; auto updated=field; for(int i=1;i<n-1;i++) updated[i]=field[i]+ratio*(field[i+1]-2*field[i]+field[i-1]); updated.front()=0; updated.back()=0; field=updated; } }
