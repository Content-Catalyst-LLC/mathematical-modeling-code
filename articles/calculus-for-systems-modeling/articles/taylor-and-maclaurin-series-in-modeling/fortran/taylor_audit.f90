program taylor_audit
  implicit none
  real(8), dimension(3) :: xs
  integer, dimension(3) :: orders
  real(8) :: x, approx, reference
  integer :: i, n, order

  xs = (/0.5d0, 1.0d0, 3.0d0/)
  orders = (/2, 10, 10/)

  print '(A)', 'function_name center x_value order approximation reference_value absolute_error warning'

  do i=1,3
    x = xs(i)
    order = orders(i)
    approx = 0.0d0
    do n=0,order
      approx = approx + (x**n) / factorial_real(n)
    end do
    reference = exp(x)
    if (abs(x) <= 2.0d0) then
      print '(A,1X,F5.1,1X,F8.4,1X,I4,1X,F14.8,1X,F14.8,1X,F14.8)', 'exp(x)', 0.0d0, x, order, approx, reference, abs(reference-approx)
    else
      print '(A,1X,F5.1,1X,F8.4,1X,I4,1X,F14.8,1X,F14.8,1X,F14.8,1X,A)', 'exp(x)', 0.0d0, x, order, approx, reference, abs(reference-approx), 'far_from_center'
    end if
  end do

contains

  function factorial_real(n) result(value)
    integer, intent(in) :: n
    integer :: k
    real(8) :: value
    value = 1.0d0
    do k=2,n
      value = value * real(k,8)
    end do
  end function factorial_real

end program
