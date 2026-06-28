const a = 3.0;
const b = 1.0;
const c = 2.0;
const d = 4.0;
const y1 = 7.0;
const y2 = 8.0;

const det = a * d - b * c;
console.log(`det(A) = ${det.toFixed(8)}`);

if (Math.abs(det) < 1e-12) {
  console.log("Matrix is singular or numerically near-singular.");
} else {
  const x1 = (d * y1 - b * y2) / det;
  const x2 = (-c * y1 + a * y2) / det;

  const r1 = a * x1 + b * x2 - y1;
  const r2 = c * x1 + d * x2 - y2;
  const residualNorm = Math.sqrt(r1 * r1 + r2 * r2);

  console.log(`Recovered state: x1 = ${x1.toFixed(8)}, x2 = ${x2.toFixed(8)}`);
  console.log(`Residual norm: ${residualNorm.toExponential(8)}`);
}
