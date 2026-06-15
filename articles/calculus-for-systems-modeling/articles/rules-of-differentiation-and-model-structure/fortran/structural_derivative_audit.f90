program structural_derivative_audit
  implicit none
  real(8), dimension(4) :: ts
  real(8) :: t, a, b
  integer :: i
  ts = (/0.0d0,5.0d0,10.0d0,20.0d0/)
  print '(A)', 'rule model_structure t derivative_value component_a component_b warning'
  do i=1,size(ts)
    t=ts(i)
    a=population_rate(t)*affluence(t)
    b=population(t)*affluence_rate(t)
    print '(A,1X,A,1X,F8.3,1X,F14.8,1X,F14.8,1X,F14.8)', 'product_rule','impact=population*affluence',t,a+b,a,b
  end do
contains
  real(8) function population(t)
    real(8), intent(in) :: t
    population=100.0d0*exp(0.01d0*t)
  end function
  real(8) function population_rate(t)
    real(8), intent(in) :: t
    population_rate=0.01d0*population(t)
  end function
  real(8) function affluence(t)
    real(8), intent(in) :: t
    affluence=2.0d0*exp(0.02d0*t)
  end function
  real(8) function affluence_rate(t)
    real(8), intent(in) :: t
    affluence_rate=0.02d0*affluence(t)
  end function
end program
