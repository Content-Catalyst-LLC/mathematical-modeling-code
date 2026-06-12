program abm_adoption_model
  implicit none

  integer, parameter :: n = 20, steps = 10
  logical :: adopted(n), next_adopted(n)
  integer :: t, i, adopted_count, local_count
  real(8), parameter :: threshold = 0.35d0

  adopted = .false.
  adopted(1) = .true.
  adopted(2) = .true.
  adopted(3) = .true.

  print '(A)', 'step adopted_count adoption_share'

  do t = 0, steps
    adopted_count = count(adopted)
    print '(I0,1X,I0,1X,F8.4)', t, adopted_count, real(adopted_count,8) / real(n,8)

    next_adopted = adopted
    do i = 1, n
      if (.not. adopted(i)) then
        local_count = 0
        if (adopted(modulo(i-3,n)+1)) local_count = local_count + 1
        if (adopted(modulo(i-2,n)+1)) local_count = local_count + 1
        if (adopted(modulo(i,n)+1)) local_count = local_count + 1
        if (adopted(modulo(i+1,n)+1)) local_count = local_count + 1
        if (real(local_count,8) / 4.0d0 >= threshold) next_adopted(i) = .true.
      end if
    end do
    adopted = next_adopted
  end do
end program abm_adoption_model
