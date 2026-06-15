program related_rates_audit
  implicit none
  real(8), dimension(5) :: ts
  real(8) :: t,h,hr,v,structural,inferred
  integer :: i
  ts = (/0.0d0,5.0d0,10.0d0,20.0d0,40.0d0/)
  print '(A)', 'time height height_rate volume structural_derivative inferred_volume_rate'
  do i=1,size(ts)
    t=ts(i); h=height_path(t); hr=height_rate(t); v=volume(h); structural=d_volume_d_height(h); inferred=structural*hr
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6)', t,h,hr,v,structural,inferred
  end do
contains
  real(8) function volume(h)
    real(8), intent(in) :: h
    volume=12.0d0*h*h
  end function
  real(8) function d_volume_d_height(h)
    real(8), intent(in) :: h
    d_volume_d_height=24.0d0*h
  end function
  real(8) function height_path(t)
    real(8), intent(in) :: t
    height_path=2.0d0 + 0.08d0*t
  end function
  real(8) function height_rate(t)
    real(8), intent(in) :: t
    height_rate=0.08d0
  end function
end program
