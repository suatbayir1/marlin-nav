# PlanValidationError, ExecutionError gibi custom hata sınıfları
# src/core/exceptions.py

class HybridPlannerError(Exception):
    """LLM-PDDL-RAG hibrit planlama sistemi için temel hata sınıfı."""
    pass


class DSLSyntaxError(HybridPlannerError):
    """LLM tarafından üretilen Pythonic DSL sözdizimi veya aksiyon adı geçersiz olduğunda fırlatılır."""
    pass


class PlanValidationError(HybridPlannerError):
    """PDDL motoru (Fast Downward) planın ön koşullarını (preconditions) reddettiğinde fırlatılır."""
    pass


class SimulationExecutionError(HybridPlannerError):
    """AI2-THOR simülasyonu sırasında fiziksel bir yürütme hatası oluştuğunda fırlatılır."""
    pass