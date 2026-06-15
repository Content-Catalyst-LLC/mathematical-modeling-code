function productRule(a: number, b: number, da: number, db: number) {
  const contributionFromA = da * b;
  const contributionFromB = a * db;
  return { contributionFromA, contributionFromB, totalDerivative: contributionFromA + contributionFromB };
}

console.log(productRule(120.0, 1.5, 4.0, 0.03));
