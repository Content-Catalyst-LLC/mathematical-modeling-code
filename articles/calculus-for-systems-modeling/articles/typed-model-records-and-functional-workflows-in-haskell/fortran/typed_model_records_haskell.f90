program typed_model_records_haskell
  implicit none

  type :: ModelParameters
    real(8) :: growth_rate
    real(8) :: carrying_capacity
    real(8) :: initial_stock
    real(8) :: time_step
    real(8) :: horizon
  end type

  type :: ModelState
    real(8) :: model_time
    real(8) :: stock
  end type

  type(ModelParameters) :: p
  type(ModelState) :: s

  p%growth_rate = 0.35d0
  p%carrying_capacity = 100.0d0
  p%initial_stock = 10.0d0
  p%time_step = 0.25d0
  p%horizon = 20.0d0

  s%model_time = 0.0d0
  s%stock = p%initial_stock

  do while (s%model_time < p%horizon)
    call step_logistic(p, s)
  end do

  print '(A)', 'model_use growth_rate carrying_capacity initial_stock time_step horizon final_time final_stock'
  print '(A,7F16.8)', 'governance_review ', p%growth_rate, p%carrying_capacity, p%initial_stock, p%time_step, p%horizon, s%model_time, s%stock

contains
  subroutine step_logistic(params, state)
    type(ModelParameters), intent(in) :: params
    type(ModelState), intent(inout) :: state
    real(8) :: dx
    dx = params%growth_rate * state%stock * (1.0d0 - state%stock / params%carrying_capacity)
    state%model_time = state%model_time + params%time_step
    state%stock = state%stock + params%time_step * dx
  end subroutine
end program
