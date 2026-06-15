#lang racket

(define (product-rule a b da db)
  (define ca (* da b))
  (define cb (* a db))
  (hash 'contribution-from-a ca
        'contribution-from-b cb
        'total-derivative (+ ca cb)))

(displayln (product-rule 120.0 1.5 4.0 0.03))
