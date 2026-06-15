#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define PI 3.14159265358979323846

void path_point(double t, double* x, double* y){ *x = t; *y = sin(t); }
double scalar_field(double x, double y){ (void)x; return 1.0 + y*y; }
void vector_field(double x, double y, double* vx, double* vy){ (void)y; *vx = 1.0; *vy = x; }
double distance_between(double x1,double y1,double x2,double y2){ return sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)); }
double dot(double ax,double ay,double bx,double by){ return ax*bx + ay*by; }

void audit(double step, const char* scenario){
  int count = (int)((2.0*PI)/step) + 1;
  double path_len = 0.0, scalar_total = 0.0, vector_total = 0.0, align_sum = 0.0, max_seg = 0.0;
  for(int i=0; i<count-1; i++){
    double t = i * step;
    double x1,y1,x2,y2,vx,vy;
    path_point(t, &x1, &y1);
    path_point(t+step, &x2, &y2);
    double dx = x2-x1, dy = y2-y1;
    double seg = distance_between(x1,y1,x2,y2);
    vector_field(x1,y1,&vx,&vy);
    double term = dot(vx,vy,dx,dy);
    path_len += seg;
    scalar_total += scalar_field(x1,y1) * seg;
    vector_total += term;
    align_sum += term / fmax(seg, 1e-12);
    if(seg > max_seg) max_seg = seg;
  }
  const char* warning = step > 0.5 ? "Time step is coarse; path turns and field variation may be undersampled." : "Synthetic line-integral audit; document path field units and interpolation.";
  printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%s\n", scenario, step, count, path_len, scalar_total, vector_total, align_sum/(count-1), max_seg, "path r(t)=<t,sin(t)>", warning);
}

int main(void){
  printf("scenario,time_step,point_count,path_length,scalar_line_integral,vector_line_integral,average_alignment,maximum_segment_length,path_description,warning\n");
  audit(1.0, "coarse_path");
  audit(0.5, "medium_path");
  audit(0.25, "fine_path");
  return EXIT_SUCCESS;
}
