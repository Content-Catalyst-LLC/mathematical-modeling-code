program differentiability_diagnostics
  implicit none

  real(8), dimension(5) :: h_values
  integer :: i

  h_values = (/ 1.0d0, 0.5d0, 0.25d0, 0.125d0, 0.0625d0 /)

  print '(A)', 'function_name x0 h forward backward central one_sided_gap kink_flag'

  do i = 1, size(h_values)
    call emit('smooth_exp_response', 5.0d0, h_values(i), 1)
  end do

  do i = 1, size(h_values)
    call emit('kink_abs_response', 0.0d0, h_values(i), 2)
  end do

contains

  real(8) function smooth_response(x)
    real(8), intent(in) :: x
    smooth_response = exp(0.2d0 * x)
  end function smooth_response

  real(8) function kink_response(x)
    real(8), intent(in) :: x
    kink_response = abs(x)
  end function kink_response

  subroutine emit(name, x0, h, kind)
    character(len=*), intent(in) :: name
    real(8), intent(in) :: x0, h
    integer, intent(in) :: kind
    real(8) :: fwd, bwd, cen, gap
    character(len=5) :: flag

    if (kind == 1) then
      fwd = (smooth_response(x0 + h) - smooth_response(x0)) / h
      bwd = (smooth_response(x0) - smooth_response(x0 - h)) / h
      cen = (smooth_response(x0 + h) - smooth_response(x0 - h)) / (2.0d0 * h)
    else
      fwd = (kink_response(x0 + h) - kink_response(x0)) / h
      bwd = (kink_response(x0) - kink_response(x0 - h)) / h
      cen = (kink_response(x0 + h) - kink_response(x0 - h)) / (2.0d0 * h)
    end if

    gap = abs(fwd - bwd)
    if (gap > 0.5d0) then
      flag = 'true'
    else
      flag = 'false'
    end if

    print '(A,1X,F8.4,1X,F8.4,1X,F12.6,1X,F12.6,1X,F12.6,1X,F12.6,1X,A)', &
      trim(name), x0, h, fwd, bwd, cen, gap, trim(flag)
  end subroutine emit

end program differentiability_diagnostics
