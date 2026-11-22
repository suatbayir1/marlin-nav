(define (problem ai2thor-task)
        (:domain multi-robot-indoor)

        (:objects
            Robot1 - agent
            countertop fridge kitchen - location
            apple - item
        )

        (:init
            (at-agent Robot1 kitchen)
    (at-object apple countertop)
    (closed fridge)
    (hand-empty Robot1)
    (openable fridge)
        )

        (:goal
            (and
              (at-object apple fridge)
      (closed fridge)
            )
        )
        )
