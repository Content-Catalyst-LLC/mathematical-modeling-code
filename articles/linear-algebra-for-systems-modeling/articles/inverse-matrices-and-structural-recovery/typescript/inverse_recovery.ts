const a = 3;
const b = 1;
const c = 2;
const d = 4;

const y1 = 7;
const y2 = 8;

const det = a * d - b * c;

if (det === 0) {
  console.log("Matrix is singular; recovery is not unique.");
} else {
  const x1 = (d * y1 - b * y2) / det;
  const x2 = (-c * y1 + a * y2) / det;
  console.log(`Recovered state: x1 = ${x1.toFixed(2)}, x2 = ${x2.toFixed(2)}`);
}
