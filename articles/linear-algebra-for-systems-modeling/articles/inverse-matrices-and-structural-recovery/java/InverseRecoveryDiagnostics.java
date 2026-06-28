public class InverseRecoveryDiagnostics {
    public static void main(String[] args) {
        double a = 3.0, b = 1.0, c = 2.0, d = 4.0;
        double y1 = 7.0, y2 = 8.0;

        double det = a * d - b * c;
        System.out.printf("det(A) = %.8f%n", det);

        if (Math.abs(det) < 1e-12) {
            System.out.println("Matrix is singular or numerically near-singular.");
            return;
        }

        double x1 = (d * y1 - b * y2) / det;
        double x2 = (-c * y1 + a * y2) / det;

        double r1 = a * x1 + b * x2 - y1;
        double r2 = c * x1 + d * x2 - y2;
        double residualNorm = Math.sqrt(r1 * r1 + r2 * r2);

        System.out.printf("Recovered state: x1 = %.8f, x2 = %.8f%n", x1, x2);
        System.out.printf("Residual norm: %.8e%n", residualNorm);
    }
}
