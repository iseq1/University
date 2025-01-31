(define (problem vacuum-problem)
    (:domain vacuum-cleaner)

    (:objects 
        region_1-1 region_1-2 region_1-3
        region_2-1 region_2-2 region_2-3
        region_3-1 region_3-2 region_3-3 - region
        cleaner1 - cleaner
    )

    (:init
        (cleaner-at cleaner1 region_3-1)

        (above region_1-1 region_2-1)
        (above region_1-2 region_2-2)
        (above region_1-3 region_2-3)
        (below region_2-1 region_1-1)
        (below region_2-2 region_1-2)
        (below region_2-3 region_1-3)

        (above region_2-1 region_3-1)
        (above region_2-2 region_3-2)
        (above region_2-3 region_3-3)
        (below region_3-1 region_2-1)
        (below region_3-2 region_2-2)
        (below region_3-3 region_2-3)

        (right region_1-2 region_1-1)
        (right region_1-3 region_1-2)
        (right region_2-2 region_2-1)
        (right region_2-3 region_2-2)
        (right region_3-2 region_3-1)
        (right region_3-3 region_3-2)

        (left region_1-1 region_1-2)
        (left region_1-2 region_1-3)
        (left region_2-1 region_2-2)
        (left region_2-2 region_2-3)
        (left region_3-1 region_3-2)
        (left region_3-2 region_3-3)

        (region_clear region_1-1)
        (region_clear region_1-2)
        (region_clear region_1-3)
        (region_clear region_2-1)
        (region_clear region_2-2)
        (region_clear region_2-3)
        (region_clear region_3-1)
        (region_clear region_3-2)
        (region_clear region_3-3)

        (dirty region_1-1)
        (dirty region_1-2)
        (dirty region_1-3)
        (dirty region_2-1)
        (dirty region_2-2)
        (dirty region_3-3)
    )

    (:goal (and
        (cleaned region_1-1)
        (cleaned region_1-2)
        (cleaned region_1-3)
        (cleaned region_2-1)
        (cleaned region_2-2)
        (cleaned region_3-3)
        (cleaner-at cleaner1 region_3-1)
    ))
)