program scaling_units_nondimensionalization
  implicit none
  print '(A)', 'record_type name value unit interpretation warning'
  print '(A)', 'unit_record population_stock 40 state_units synthetic_teaching_value unit_warning'
  print '(A)', 'unit_record carrying_capacity 100 state_units synthetic_teaching_capacity capacity_scale_warning'
  print '(A)', 'unit_record growth_rate 0.35 per_time_unit synthetic_teaching_rate rate_unit_warning'
  print '(A)', 'scale_record stock_scale 100 state_units normalize_population_stock scale_warning'
  print '(A)', 'nondimensional_record scaled_stock 0.4 dimensionless fraction_of_capacity documented_scale_required'
end program
