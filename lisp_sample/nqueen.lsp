(define nqueen
    (lambda (n)
        (nqueen2 n 1 nil)))

(define nqueen2
    (lambda (n y board)
        (if (> y n)
            nil
            (if (or (member board y) (diagonal 1 y board))
                (nqueen2 n (+ y 1) board)
                (append
                    (if (eq? (length board) (- n 1))
                        (list (cons y board))
                        (nqueen2 n 1 (cons y board))
                    )
                    (nqueen2 n (+ y 1) board)
                )
            )
        )
    )
)

(define diagonal
    (lambda (x queen board)
        (if (null board)
            nil
            (if (eq? (abs (- (car board) queen)) x)
                T
                (diagonal (+ x 1) queen (cdr board))
            )
        )
    )
)
