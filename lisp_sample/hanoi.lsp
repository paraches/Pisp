(define hanoi
    (lambda (n i j k)
        (begin
            (if (> n 1)
                (hanoi (- n 1) i k j)
            )
            (fprint '"move %dth from %d to %d" n i j)
            (if (> n 1)
                (hanoi (- n 1) k j i)
            )
        )
    )
)

(hanoi 3 1 2 3)
