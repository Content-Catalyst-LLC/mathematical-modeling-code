row_count = 3
column_count = 3
rank_value = 3
nullity_value = 0
input_state = "100.000000;60.000000;30.000000"
output_state = "126.000000;75.500000;42.000000"
input_norm = 120.415946
output_norm = 152.750205
amplification_ratio = 1.268531

println("system_name,row_count,column_count,input_state,output_state,rank,nullity,input_norm,output_norm,amplification_ratio,warning")
println(join((
    "three_component_system_response",
    row_count,
    column_count,
    input_state,
    output_state,
    rank_value,
    nullity_value,
    input_norm,
    output_norm,
    amplification_ratio,
    "Matrix action requires row meanings column meanings units scaling and sensitivity review."
), ","))
