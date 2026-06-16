initialize_field <- function(grid_points) { field <- rep(0, grid_points); field[[ceiling(grid_points/2)]] <- 1; field }
update_diffusion <- function(field, ratio) {
  updated <- field
  for (i in 2:(length(field)-1)) updated[[i]] <- field[[i]] + ratio * (field[[i+1]] - 2*field[[i]] + field[[i-1]])
  updated[[1]] <- 0; updated[[length(updated)]] <- 0; updated
}
grid_points <- 61; diffusivity <- 0.08; dx <- 1; dt <- 0.2; steps <- 120
ratio <- diffusivity * dt / (dx^2)
status <- ifelse(ratio <= 0.5, "stable_for_basic_explicit_1d_diffusion", "unstable_risk")
field <- initialize_field(grid_points); rows <- list()
for (step in 0:steps) {
  rows[[length(rows)+1]] <- data.frame(step=step,time=step*dt,center_value=field[[ceiling(grid_points/2)]],total_mass=sum(field)*dx,max_value=max(field),left_boundary=field[[1]],right_boundary=field[[length(field)]],diffusion_ratio=ratio,stability_status=status)
  field <- update_diffusion(field, ratio)
}
dir.create("outputs/tables", recursive=TRUE, showWarnings=FALSE)
write.csv(do.call(rbind, rows), "outputs/tables/r_finite_difference_audit.csv", row.names=FALSE)
print(head(do.call(rbind, rows)))
