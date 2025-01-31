(define (domain vacuum-cleaner)

    (:requirements :typing)

    (:types 
        cleaner region - object
    )

    (:predicates
        (cleaner-at ?c - cleaner ?x - region)
        (region_clear ?x - region)
        (above ?x - region ?y - region)
        (below ?x - region ?y - region)
        (right ?x - region ?y - region)
        (left ?x - region ?y - region)
        (cleaned ?x - region)
        (dirty ?x - region)
    )

    (:action suck
        :parameters (?r - cleaner ?x - region)
        :precondition (and
            (dirty ?x)
            (cleaner-at ?r ?x)
        )
        :effect (and
            (cleaned ?x)
            (not (dirty ?x))
        )
    )

    (:action move_up
        :parameters (?r - cleaner ?x - region ?y - region)
        :precondition (and
            (above ?x ?y)
            (cleaner-at ?r ?y)
            (region_clear ?x)
        )
        :effect (and
            (cleaner-at ?r ?x)
            (not (cleaner-at ?r ?y))
        )
    )

    (:action move_down
        :parameters (?r - cleaner ?x - region ?y - region)
        :precondition (and
            (below ?x ?y)
            (cleaner-at ?r ?y)
            (region_clear ?x)
        )
        :effect (and
            (cleaner-at ?r ?x)
            (not (cleaner-at ?r ?y))
        )
    )

    (:action move_left
        :parameters (?r - cleaner ?x - region ?y - region)
        :precondition (and
            (left ?x ?y)
            (cleaner-at ?r ?y)
            (region_clear ?x)
        )
        :effect (and
            (cleaner-at ?r ?x)
            (not (cleaner-at ?r ?y))
        )
    )

    (:action move_right
        :parameters (?r - cleaner ?x - region ?y - region)
        :precondition (and
            (right ?x ?y)
            (cleaner-at ?r ?y)
            (region_clear ?x)
        )
        :effect (and
            (cleaner-at ?r ?x)
            (not (cleaner-at ?r ?y))
        )
    )
)