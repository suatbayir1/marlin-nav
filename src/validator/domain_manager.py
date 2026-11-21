# PDDL Domain dosyalarını (domain.md) okuyan/yöneten sınıf
# src/validator/domain_manager.py

from pathlib import Path
from typing import Dict, List, Set


class DomainManager:
    """
    Çoklu robot iç mekan görev planlaması için PDDL Domain tanımını (domain.pddl)
    yönetir ve aksi takdirde eylemlerin ön koşul/etki kurallarını sağlar.
    """

    DOMAIN_NAME = "multi-robot-indoor"

    DOMAIN_PDDL = """(define (domain multi-robot-indoor)
  (:requirements :strips :typing :negative-preconditions)

  (:types
    agent location item
  )

  (:predicates
    (at-agent ?a - agent ?l - location)
    (at-object ?o - item ?l - location)
    (holding ?a - agent ?o - item)
    (hand-empty ?a - agent)
    (openable ?l - location)
    (opened ?l - location)
    (closed ?l - location)
    (toggleable ?o - item)
    (is-on ?o - item)
    (searched ?l - location ?o - item)
  )

  (:action navigate
    :parameters (?a - agent ?from - location ?to - location)
    :precondition (and
      (at-agent ?a ?from)
    )
    :effect (and
      (not (at-agent ?a ?from))
      (at-agent ?a ?to)
    )
  )

  (:action open
    :parameters (?a - agent ?l - location)
    :precondition (and
      (at-agent ?a ?l)
      (openable ?l)
      (closed ?l)
    )
    :effect (and
      (not (closed ?l))
      (opened ?l)
    )
  )

  (:action close
    :parameters (?a - agent ?l - location)
    :precondition (and
      (at-agent ?a ?l)
      (openable ?l)
      (opened ?l)
    )
    :effect (and
      (not (opened ?l))
      (closed ?l)
    )
  )

  (:action pickup
    :parameters (?a - agent ?o - item ?l - location)
    :precondition (and
      (at-agent ?a ?l)
      (at-object ?o ?l)
      (hand-empty ?a)
    )
    :effect (and
      (not (at-object ?o ?l))
      (not (hand-empty ?a))
      (holding ?a ?o)
    )
  )

  (:action put
    :parameters (?a - agent ?o - item ?l - location)
    :precondition (and
      (at-agent ?a ?l)
      (holding ?a ?o)
      (or (not (openable ?l)) (opened ?l))
    )
    :effect (and
      (not (holding ?a ?o))
      (hand-empty ?a)
      (at-object ?o ?l)
    )
  )

  (:action search
    :parameters (?a - agent ?l - location ?o - item)
    :precondition (and
      (at-agent ?a ?l)
    )
    :effect (and
      (searched ?l ?o)
    )
  )

  (:action toggle-on
    :parameters (?a - agent ?o - item ?l - location)
    :precondition (and
      (at-agent ?a ?l)
      (at-object ?o ?l)
      (toggleable ?o)
    )
    :effect (and
      (is-on ?o)
    )
  )

  (:action toggle-off
    :parameters (?a - agent ?o - item ?l - location)
    :precondition (and
      (at-agent ?a ?l)
      (at-object ?o ?l)
      (toggleable ?o)
      (is-on ?o)
    )
    :effect (and
      (not (is-on ?o))
    )
  )
)
"""

    def __init__(self, pddl_output_dir: str = "data/pddl"):
        self.output_dir = Path(pddl_output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.domain_file_path = self.output_dir / "domain.pddl"

    def save_domain_file(self) -> Path:
        """Standart multi-robot domain.pddl dosyasını diske yazar."""
        self.domain_file_path.write_text(self.DOMAIN_PDDL.strip() + "\n", encoding="utf-8")
        return self.domain_file_path

    def get_domain_text(self) -> str:
        return self.DOMAIN_PDDL