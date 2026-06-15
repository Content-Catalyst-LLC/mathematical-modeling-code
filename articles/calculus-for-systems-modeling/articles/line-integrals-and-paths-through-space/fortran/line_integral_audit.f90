program line_integral_audit
  implicit none
  real(8), parameter :: pi = 3.14159265358979323846d0
  print '(A)', 'scenario time_step point_count path_length scalar_line_integral vector_line_integral average_alignment maximum_segment_length path_description warning'
  call audit(1.0d0, 'coarse_path')
  call audit(0.5d0, 'medium_path')
  call audit(0.25d0, 'fine_path')
contains
  subroutine path_point(t, x, y)
    real(8), intent(in) :: t
    real(8), intent(out) :: x, y
    x = t
    y = sin(t)
  end subroutine

  real(8) function scalar_field(x,y)
    real(8), intent(in) :: x,y
    scalar_field = 1.0d0 + y*y
  end function

  subroutine vector_field(x,y,vx,vy)
    real(8), intent(in) :: x,y
    real(8), intent(out) :: vx,vy
    vx = 1.0d0
    vy = x
  end subroutine

  real(8) function dist(x1,y1,x2,y2)
    real(8), intent(in) :: x1,y1,x2,y2
    dist = sqrt((x2-x1)**2 + (y2-y1)**2)
  end function

  subroutine audit(step, scenario)
    real(8), intent(in) :: step
    character(len=*), intent(in) :: scenario
    integer :: i, count
    real(8) :: x1,y1,x2,y2,dx,dy,vx,vy,seg,term,path_len,scalar_total,vector_total,align_sum,max_seg
    character(len=32) :: warning
    count = int((2.0d0*pi)/step) + 1
    path_len = 0.0d0
    scalar_total = 0.0d0
    vector_total = 0.0d0
    align_sum = 0.0d0
    max_seg = 0.0d0
    do i = 0, count-2
      call path_point(i*step, x1, y1)
      call path_point((i+1)*step, x2, y2)
      dx = x2 - x1
      dy = y2 - y1
      seg = dist(x1,y1,x2,y2)
      call vector_field(x1,y1,vx,vy)
      term = vx*dx + vy*dy
      path_len = path_len + seg
      scalar_total = scalar_total + scalar_field(x1,y1) * seg
      vector_total = vector_total + term
      align_sum = align_sum + term / max(seg, 1.0d-12)
      max_seg = max(max_seg, seg)
    end do
    if (step > 0.5d0) then
      warning = 'coarse_path'
    else
      warning = 'synthetic_line_integral'
    end if
    print '(A,1X,F8.3,1X,I8,5F14.6,1X,A,1X,A)', trim(scenario), step, count, path_len, scalar_total, vector_total, align_sum/(count-1), max_seg, 'path', trim(warning)
  end subroutine
end program
