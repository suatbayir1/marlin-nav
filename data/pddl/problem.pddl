(define (problem ep_001)
        (:domain multi-robot-indoor)

        (:objects
            Robot1 Robot2 - agent
            countertop fridge kitchen - location
            apple - item
        )

        (:init
            (at-agent Robot1 kitchen)
    (at-agent Robot2 kitchen)
    (at-object apple countertop)
    (closed fridge)
    (hand-empty Robot1)
    (hand-empty Robot2)
    (openable fridge)
        )

        (:goal
            (and
              (at-object apple fridge)
      (closed fridge)
            )
        )
        )
