program second_order_oscillation_audit
  implicit none
  call simulate('underdamped_unforced', 0.2d0, 0.0d0)
  call simulate('forced_near_resonance', 0.1d0, 0.2d0)
contains
  real(8) function forcing_function(t, amplitude, frequency)
    real(8), intent(in) :: t, amplitude, frequency
    forcing_function = amplitude*cos(frequency*t)
  end function
  real(8) function accel(x, v, t, damping, natural, force_amp, force_freq)
    real(8), intent(in) :: x, v, t, damping, natural, force_amp, force_freq
    accel = forcing_function(t, force_amp, force_freq) - 2.0d0*damping*natural*v - natural*natural*x
  end function
  subroutine simulate(label, damping, force_amp)
    character(len=*), intent(in) :: label
    real(8), intent(in) :: damping, force_amp
    real(8) :: x, v, natural, force_freq, dt, t, a, force
    integer :: n, steps
    x = 1.0d0; v = 0.0d0; natural = 1.0d0; force_freq = 1.0d0; dt = 0.02d0; steps = 500
    do n = 0, steps
      t = n*dt
      a = accel(x, v, t, damping, natural, force_amp, force_freq)
      force = forcing_function(t, force_amp, force_freq)
      print '(A,8F12.6,1X,A)', trim(label), t, x, v, a, damping, natural, force, 0.0d0, 'explicit_euler'
      v = v + dt*a
      x = x + dt*v
    end do
  end subroutine
end program
