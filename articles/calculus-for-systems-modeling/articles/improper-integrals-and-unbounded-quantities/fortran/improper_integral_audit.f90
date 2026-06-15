program improper_integral_audit
  implicit none
  real(8), dimension(5) :: cutoffs
  real(8) :: reference, cutoff, truncated, tail_error
  integer :: i

  cutoffs = (/2.0d0,4.0d0,8.0d0,12.0d0,20.0d0/)
  reference = 1.0d0/0.4d0

  print '(A)', 'cutoff truncated_value reference_value tail_error'
  do i=1,5
    cutoff = cutoffs(i)
    truncated = trap(0.0d0, cutoff, 4000)
    tail_error = reference - truncated
    print '(F8.3,1X,F14.6,1X,F14.6,1X,F14.6)', cutoff, truncated, reference, tail_error
  end do

contains
  real(8) function tail_function(x)
    real(8), intent(in) :: x
    tail_function = exp(-0.4d0*x)
  end function

  real(8) function trap(a,b,n)
    real(8), intent(in) :: a,b
    integer, intent(in) :: n
    real(8) :: dx, x0, x1
    integer :: j
    trap = 0.0d0
    dx = (b-a)/real(n,8)
    do j=0,n-1
      x0 = a + dx*real(j,8)
      x1 = x0 + dx
      trap = trap + 0.5d0*(tail_function(x0)+tail_function(x1))*dx
    end do
  end function
end program
