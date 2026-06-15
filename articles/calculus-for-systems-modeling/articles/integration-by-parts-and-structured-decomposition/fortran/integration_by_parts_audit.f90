program integration_by_parts_audit
  implicit none
  real(8) :: a, b, direct, residual, boundary, decomposed, decomp_resid
  integer :: n

  a = 0.0d0
  b = 4.0d0
  n = 800

  direct = trap_direct(a,b,n)
  residual = trap_residual(a,b,n)
  boundary = u_value(b)*v_value(b) - u_value(a)*v_value(a)
  decomposed = boundary - residual
  decomp_resid = direct - decomposed

  print '(A)', 'interval_start interval_end direct_integral boundary_term residual_integral decomposed_value decomposition_residual'
  print '(F8.3,1X,F8.3,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6,1X,F14.6)', a,b,direct,boundary,residual,decomposed,decomp_resid

contains
  real(8) function u_value(x)
    real(8), intent(in) :: x
    u_value = 1.0d0 + x
  end function

  real(8) function u_prime(x)
    real(8), intent(in) :: x
    u_prime = 1.0d0
  end function

  real(8) function v_value(x)
    real(8), intent(in) :: x
    v_value = exp(-0.3d0*x) * sin(x)
  end function

  real(8) function v_prime(x)
    real(8), intent(in) :: x
    v_prime = exp(-0.3d0*x) * (cos(x) - 0.3d0*sin(x))
  end function

  real(8) function trap_direct(a0,b0,n0)
    real(8), intent(in) :: a0,b0
    integer, intent(in) :: n0
    real(8) :: dx, x0, x1
    integer :: i
    trap_direct = 0.0d0
    dx = (b0-a0)/real(n0,8)
    do i=0,n0-1
      x0 = a0 + dx*real(i,8)
      x1 = x0 + dx
      trap_direct = trap_direct + 0.5d0*((u_value(x0)*v_prime(x0))+(u_value(x1)*v_prime(x1)))*dx
    end do
  end function

  real(8) function trap_residual(a0,b0,n0)
    real(8), intent(in) :: a0,b0
    integer, intent(in) :: n0
    real(8) :: dx, x0, x1
    integer :: i
    trap_residual = 0.0d0
    dx = (b0-a0)/real(n0,8)
    do i=0,n0-1
      x0 = a0 + dx*real(i,8)
      x1 = x0 + dx
      trap_residual = trap_residual + 0.5d0*((v_value(x0)*u_prime(x0))+(v_value(x1)*u_prime(x1)))*dx
    end do
  end function
end program
