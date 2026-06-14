program engineering_design_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: width(n), height(n), span(n), load(n), allowable(n), density(n)
  real(8) :: stress(n), margin(n), safety_factor(n), mass(n)
  integer :: i

  keys = (/ 'light_design                  ', 'balanced_design               ', 'stiff_design                  ', 'overloaded_case               ' /)
  width = (/ 0.08d0, 0.10d0, 0.12d0, 0.10d0 /)
  height = (/ 0.16d0, 0.18d0, 0.22d0, 0.18d0 /)
  span = (/ 3.0d0, 3.0d0, 3.0d0, 3.0d0 /)
  load = (/ 4200.0d0, 4200.0d0, 4200.0d0, 7000.0d0 /)
  allowable = (/ 145000000.0d0, 145000000.0d0, 145000000.0d0, 145000000.0d0 /)
  density = (/ 7850.0d0, 7850.0d0, 7850.0d0, 7850.0d0 /)

  print '(A)', 'key max_stress_pa stress_margin_pa safety_factor estimated_mass_kg passes_stress_constraint'

  do i = 1, n
    call evaluate_beam(width(i), height(i), span(i), load(i), allowable(i), density(i), stress(i), margin(i), safety_factor(i), mass(i))
    print '(A,1X,F12.3,1X,F12.3,1X,F8.4,1X,F10.3,1X,L1)', trim(keys(i)), stress(i), margin(i), safety_factor(i), mass(i), stress(i) <= allowable(i)
  end do

contains

  subroutine evaluate_beam(width_m, height_m, span_m, load_n, allowable_stress, material_density, stress, margin, safety_factor, mass)
    implicit none
    real(8), intent(in) :: width_m, height_m, span_m, load_n, allowable_stress, material_density
    real(8), intent(out) :: stress, margin, safety_factor, mass
    real(8) :: moment, inertia, c_value

    moment = load_n * span_m / 4.0d0
    inertia = width_m * height_m**3 / 12.0d0
    c_value = height_m / 2.0d0
    stress = moment * c_value / inertia
    margin = allowable_stress - stress
    safety_factor = allowable_stress / stress
    mass = width_m * height_m * span_m * material_density
  end subroutine evaluate_beam

end program engineering_design_summary
