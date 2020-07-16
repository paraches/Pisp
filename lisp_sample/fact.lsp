(define fact (lambda (x) (cond ((eq? x 0) 1) (T (* (fact (- x 1)) x)))))
(fact 5)
