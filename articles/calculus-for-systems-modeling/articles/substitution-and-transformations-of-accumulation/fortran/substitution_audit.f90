program substitution_audit
  implicit none
  real(8) :: a, b, ua, ub, direct, transformed, residual
  integer :: n

  a = 1.0d0
  b = 3.0d0
  ua = g_value(a)
  ub = g_value(b)
  n = 400

  direct = trap_x(a, b, n)
  transformed = trap_u(ua, ub, n)
  residual = direct - transformed

  print '(A)', 'original_start original_end transformed_start transformed_end direct_integral transformed_integral residual'
  print '(F8.3,1X,F8.3,1X,F8.3,1X,F8.3,1X,F14.6,1X,F14.6,1X,F14.6)', a,b,ua,ub,direct,transformed,residual

contains
  real(8) function g_value(x)
    real(8), intent(in) :: x
    g_value = x*x + 1.0d0
  end function

  real(8) function g_prime(x)
    real(8), intent(in) :: x
    g_prime = 2.0d0*x
  end function

  real(8) function f_value(u)
    real(8), intent(in) :: u
    f_value = sqrt(u)
  end function

  real(8) function integrand_x(x)
    real(8), intent(in) :: x
    integrand_x = f_value(g_value(x)) * g_prime(x)
  end function

  real(8) function trap_x(a0,b0,n0)
    real(8), intent(in) :: a0,b0
    integer, intent(in) :: n0
    real(8) :: step, x0, x1
    integer :: i
    trap_x = 0.0d0
    step = (b0-a0)/real(n0,8)
    do i=0,n0-1
      x0 = a0 + step*real(i,8)
      x1 = x0 + step
      trap_x = trap_x + 0.5d0*(integrand_x(x0)+integrand_x(x1))*step
    end do
  end function

  real(8) function trap_u(a0,b0,n0)
    real(8), intent(in) :: a0,b0
    integer, intent(in) :: n0
    real(8) :: step, u0, u1
    integer :: i
    trap_u = 0.0d0
    step = (b0-a0)/real(n0,8)
    do i=0,n0-1
      u0 = a0 + step*real(i,8)
      u1 = u0 + step
      trap_u = trap_u + 0.5d0*(f_value(u0)+f_value(u1))*step
    end do
  end function
end program
