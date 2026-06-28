public class InverseRecovery {
    public static void main(String[] args) {
        double a = 3, b = 1, c = 2, d = 4;
        double y1 = 7, y2 = 8;
        double det = a * d - b * c;

        if (det == 0) {
            System.out.println("Matrix is singular; recovery is not unique.");
            return;
        }

        double x1 = (d * y1 - b * y2) / det;
        double x2 = (-c * y1 + a * y2) / det;

        System.out.printf("Recovered state: x1 = %.2f, x2 = %.2f%n", x1, x2);
    }
}
