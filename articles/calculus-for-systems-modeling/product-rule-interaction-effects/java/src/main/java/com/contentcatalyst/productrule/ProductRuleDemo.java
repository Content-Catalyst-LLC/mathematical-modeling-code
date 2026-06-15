package com.contentcatalyst.productrule;

public class ProductRuleDemo {
    record ProductContribution(double contributionFromA, double contributionFromB, double totalDerivative) {}

    static ProductContribution productRule(double a, double b, double da, double db) {
        double ca = da * b;
        double cb = a * db;
        return new ProductContribution(ca, cb, ca + cb);
    }

    public static void main(String[] args) {
        System.out.println(productRule(120.0, 1.5, 4.0, 0.03));
    }
}
