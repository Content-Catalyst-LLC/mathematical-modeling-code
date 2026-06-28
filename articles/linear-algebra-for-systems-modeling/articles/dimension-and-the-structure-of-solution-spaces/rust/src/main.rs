fn main() {
    let variable_count = 4;
    let equation_count = 3;
    let rank = 3;
    let nullity = variable_count - rank;

    println!("system_name,variable_count,equation_count,rank,nullity,likely_solution_structure,warning");
    println!(
        "four_variable_three_constraint_system,{},{},{},{},Positive-dimensional solution space if consistent,Rank and nullity are mathematical diagnostics not proof of feasibility.",
        variable_count, equation_count, rank, nullity
    );
}
