# Doğal dil girdisini alıp RAG context'i ile Pythonic DSL üretir
# src/planner/dsl_generator.py

import ast
from dataclasses import dataclass
from typing import List, Optional

from src.core.exceptions import DSLSyntaxError
from src.memory.context_builder import ContextBuilder
from src.planner.llm_agent import LLMAgent


@dataclass
class DSLStep:
    """Ayrıştırılmış tek bir Pythonic DSL komutunu temsil eden veri yapısı."""
    agent_id: str       # Örn: "Robot1"
    action: str         # Örn: "pickup"
    args: List[str]     # Örn: ["apple"]
    raw_line: str       # Örn: 'Robot1.pickup("apple")'


class DSLGenerator:
    """
    RAG bağlamını ve LLM ajanını kullanarak yapılandırılmış (structured)
    Pythonic DSL planı üretir ve sözdizimsel doğrulamadan (AST) geçirir.
    """

    ALLOWED_ACTIONS = {
        "navigate",
        "search",
        "open",
        "close",
        "pickup",
        "put",
        "toggle_on",
        "toggle_off"
    }

    def __init__(self, llm_agent: LLMAgent, context_builder: ContextBuilder):
        self.llm = llm_agent
        self.context_builder = context_builder

    def generate_structured_plan(
        self,
        task_instruction: str,
        current_state: str = "",
        error_feedback: Optional[str] = None,
        top_k: int = 4
    ) -> List[DSLStep]:
        """
        1. RAG hafızasından ilgili PDDL/API kurallarını çeker.
        2. LLM'den Pythonic DSL planı üretmesini ister.
        3. Çıktıyı AST ile ayrıştırıp yapılandırılmış DSLStep listesi döner.
        """
        rag_context = self.context_builder.build_context(
            task_instruction=task_instruction,
            current_state=current_state,
            n_results=top_k
        )

        raw_dsl = self.llm.generate_plan(
            task_instruction=task_instruction,
            rag_context=rag_context,
            error_feedback=error_feedback
        )

        return self.parse_dsl(raw_dsl)

    def parse_dsl(self, raw_dsl: str) -> List[DSLStep]:
        """
        Pythonic DSL satırlarını Python AST modülü ile güvenli şekilde ayrıştırır.
        Hatalı format veya tanımlanmamış aksiyon varsa DSLSyntaxError fırlatır.
        """
        if not raw_dsl or not raw_dsl.strip():
            raise DSLSyntaxError("LLM boş bir plan üretti.")

        steps: List[DSLStep] = []

        for line_no, line in enumerate(raw_dsl.strip().splitlines(), start=1):
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue

            try:
                tree = ast.parse(clean_line, mode="eval")
            except SyntaxError as e:
                raise DSLSyntaxError(f"Satır {line_no} sözdizimi hatası ('{clean_line}'): {e}")

            if not isinstance(tree.body, ast.Call):
                raise DSLSyntaxError(f"Satır {line_no} geçerli bir fonksiyon çağrısı değil: '{clean_line}'")

            func = tree.body.func
            if not (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)):
                raise DSLSyntaxError(
                    f"Satır {line_no} 'RobotX.action(...)' formatında olmalıdır: '{clean_line}'"
                )

            agent_id = func.value.id
            action_name = func.attr

            if action_name not in self.ALLOWED_ACTIONS:
                raise DSLSyntaxError(
                    f"Satır {line_no} tanımlanmamış aksiyon içeriyor: '{action_name}'. "
                    f"İzin verilenler: {sorted(self.ALLOWED_ACTIONS)}"
                )

            args: List[str] = []
            for arg in tree.body.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    args.append(arg.value)
                else:
                    raise DSLSyntaxError(
                        f"Satır {line_no} argümanları string olmalıdır: '{clean_line}'"
                    )

            steps.append(DSLStep(
                agent_id=agent_id,
                action=action_name,
                args=args,
                raw_line=clean_line
            ))

        return steps


# Adım 5 Entegrasyon Testi
if __name__ == "__main__":
    from src.memory.chromadb_client import VectorDatabaseClient

    db = VectorDatabaseClient(persist_directory="./chroma_db")
    context_builder = ContextBuilder(db_client=db)
    llm_agent = LLMAgent()
    generator = DSLGenerator(llm_agent=llm_agent, context_builder=context_builder)

    task = "Pick up the apple from the countertop and put it inside the fridge."
    state = "Robot1 is in kitchen. Apple is on countertop. Fridge is closed."

    structured_steps = generator.generate_structured_plan(task_instruction=task, current_state=state)

    print("=== AST İLE DOĞRULANMIŞ YAPILANDIRILMIŞ DSL ADIMLARI ===")
    for idx, step in enumerate(structured_steps, start=1):
        print(f"{idx}. Ajan: {step.agent_id} | Aksiyon: {step.action} | Parametreler: {step.args}")