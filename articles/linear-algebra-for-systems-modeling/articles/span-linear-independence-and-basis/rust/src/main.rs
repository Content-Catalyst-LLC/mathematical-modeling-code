fn determinant3x3(m: [[f64; 3]; 3]) -> f64 {
    m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
}

fn main() {
    let matrix = [
        [1.0, 0.0, 0.5],
        [0.0, 1.0, 0.5],
        [0.0, 0.0, 1.0],
    ];

    let rank = if determinant3x3(matrix).abs() > 1e-10 { 3 } else { 2 };
    let spans = rank == 3;
    let independent = rank == 3;
    let basis = spans && independent;

    println!("vector_set_name,ambient_dimension,vector_count,rank,spans_ambient_space,linearly_independent,is_basis_for_ambient_space,warning");
    println!(
        "candidate_system_basis,3,3,{},{},{},{},A mathematical basis claim does not prove real-world adequacy.",
        rank, spans, independent, basis
    );
}
