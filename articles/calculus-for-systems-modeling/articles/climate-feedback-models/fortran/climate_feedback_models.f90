program climate_feedback_models
  implicit none
  integer :: t
  real(8) :: forcing, c, weak, baseline, strong
  forcing = 3.7d0
  c = 8.0d0
  print '(A)', 'time weak_feedback baseline_feedback strong_feedback'
  do t = 0, 100, 10
    weak = (forcing/0.9d0) * (1.0d0 - exp(-(0.9d0/c)*dble(t)))
    baseline = (forcing/1.2d0) * (1.0d0 - exp(-(1.2d0/c)*dble(t)))
    strong = (forcing/1.6d0) * (1.0d0 - exp(-(1.6d0/c)*dble(t)))
    print '(I0,1X,F12.6,1X,F12.6,1X,F12.6)', t, weak, baseline, strong
  end do
end program
