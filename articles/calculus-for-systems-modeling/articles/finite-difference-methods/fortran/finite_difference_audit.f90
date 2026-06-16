program finite_difference_audit
implicit none
integer, parameter :: n=61, steps=120
integer :: s,i
real(8) :: field(n), updated(n), ratio, dx, dt, total_mass
dx=1.0d0; dt=0.2d0; ratio=0.08d0*dt/(dx*dx); field=0.0d0; field(31)=1.0d0
print '(A)', 'step time center_value total_mass diffusion_ratio'
do s=0,steps
  total_mass=sum(field)*dx
  print '(I6,4F14.6)', s, dble(s)*dt, field(31), total_mass, ratio
  updated=field
  do i=2,n-1
    updated(i)=field(i)+ratio*(field(i+1)-2.0d0*field(i)+field(i-1))
  end do
  updated(1)=0.0d0; updated(n)=0.0d0; field=updated
end do
end program
