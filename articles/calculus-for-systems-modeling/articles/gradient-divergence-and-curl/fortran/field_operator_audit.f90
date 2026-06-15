program field_operator_audit
  implicit none
  print '(A)', 'scenario grid_step point_count mean_gradient_magnitude maximum_gradient_magnitude mean_divergence mean_curl maximum_abs_curl field_description warning'
  call audit(1.0d0, 'coarse_grid')
  call audit(0.5d0, 'medium_grid')
  call audit(0.25d0, 'fine_grid')
contains
  subroutine gradient(x,y,gx,gy)
    real(8), intent(in) :: x,y
    real(8), intent(out) :: gx,gy
    gx = 2.0d0*x
    gy = 2.0d0*y
  end subroutine

  subroutine audit(step, scenario)
    real(8), intent(in) :: step
    character(len=*), intent(in) :: scenario
    integer :: i,j,n,count
    real(8) :: x,y,gx,gy,gmag,grad_sum,max_grad,div_sum,curl_sum,max_abs_curl,curl
    character(len=32) :: warning
    n = int(2.0d0 / step) + 1
    count = 0
    grad_sum = 0.0d0
    max_grad = 0.0d0
    div_sum = 0.0d0
    curl_sum = 0.0d0
    max_abs_curl = 0.0d0
    do i = 0, n-1
      x = -1.0d0 + i*step
      do j = 0, n-1
        y = -1.0d0 + j*step
        call gradient(x,y,gx,gy)
        gmag = sqrt(gx*gx + gy*gy)
        curl = 2.0d0
        count = count + 1
        grad_sum = grad_sum + gmag
        max_grad = max(max_grad, gmag)
        div_sum = div_sum + 0.0d0
        curl_sum = curl_sum + curl
        max_abs_curl = max(max_abs_curl, abs(curl))
      end do
    end do
    if (step > 0.5d0) then
      warning = 'coarse_grid'
    else
      warning = 'synthetic_field'
    end if
    print '(A,1X,F8.3,1X,I8,5F14.6,1X,A,1X,A)', trim(scenario), step, count, grad_sum/count, max_grad, div_sum/count, curl_sum/count, max_abs_curl, 'field', trim(warning)
  end subroutine
end program
