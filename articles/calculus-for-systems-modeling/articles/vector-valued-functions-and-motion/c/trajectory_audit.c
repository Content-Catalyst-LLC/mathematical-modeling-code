#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define PI 3.14159265358979323846

void position(double t, double* x, double* y){ *x = t; *y = sin(t); }
double distance_between(double x1,double y1,double x2,double y2){ return sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)); }

void audit(double step, const char* scenario){
  int count = (int)((2.0*PI)/step) + 1;
  double prev_x, prev_y, first_x, first_y, last_x, last_y;
  double arc = 0.0, speed_sum = 0.0, speed_max = 0.0;
  position(0.0, &first_x, &first_y);
  prev_x = first_x; prev_y = first_y;
  for(int i=1; i<count; i++){
    double t = i * step;
    double x,y;
    position(t, &x, &y);
    double seg = distance_between(prev_x, prev_y, x, y);
    double speed = seg / step;
    arc += seg;
    speed_sum += speed;
    if(speed > speed_max) speed_max = speed;
    prev_x = x; prev_y = y;
  }
  last_x = prev_x; last_y = prev_y;
  double disp = distance_between(first_x, first_y, last_x, last_y);
  double eff = disp / fmax(arc, 1e-12);
  const char* warning = step > 0.5 ? "Time step is coarse; turns and speed variation may be undersampled." : "Synthetic trajectory audit; document units parameter meaning and sampling.";
  printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%s\n", scenario, step, count, arc, disp, eff, speed_sum/(count-1), speed_max, "trajectory r(t)=<t,sin(t)>", warning);
}

int main(void){
  printf("scenario,time_step,point_count,approximate_arc_length,displacement_magnitude,path_efficiency,average_speed,maximum_speed,domain_description,warning\n");
  audit(1.0, "coarse_time_step");
  audit(0.5, "medium_time_step");
  audit(0.25, "fine_time_step");
  return EXIT_SUCCESS;
}
