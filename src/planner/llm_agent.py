# LLaMA 3/Mistral 7B veya GPT-4o API entegrasyonu
# RAG'dan gelen bağlamı (ContextBuilder) alıp LLM'e gönderen ve Pythonic DSL planı üreten sınıf.
import os
import sys
import yaml
from pathlib import Path
from typing import Optional
from openai import OpenAI
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from src.memory.chromadb_client import VectorDatabaseClient
from src.memory.context_builder import ContextBuilder

class LLMAgent:
    def __init__(
        self,
        config_path: str = None,
        prompts_path: str = None
    ):
        """
        Merkezi Planlayıcı (Central Planner) LLM arayüzü.
        RAG bağlamını ve görev talimatını birleştirerek Pythonic DSL üretir.
        """
        config_path = config_path or PROJECT_ROOT / "config/config.yaml"
        prompts_path = prompts_path or PROJECT_ROOT / "config/prompts.yaml"
        self.config = self._load_yaml(str(config_path))
        self.prompts = self._load_yaml(str(prompts_path))

        llm_cfg = self.config.get("llm", {})
        self.provider = llm_cfg.get("provider", "mock")
        self.model_name = llm_cfg.get("model_name", "mistral-7b")
        self.base_url = llm_cfg.get("base_url", "http://localhost:11434/v1")
        self.api_key_env = llm_cfg.get("api_key_env", "OPENAI_API_KEY")
        self.temperature = llm_cfg.get("temperature", 0.1)
        self.max_tokens = llm_cfg.get("max_tokens", 512)

    def _load_yaml(self, path_str: str) -> dict:
        path = Path(path_str)
        if not path.exists():
            raise FileNotFoundError(f"Konfigürasyon dosyası bulunamadı: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def build_prompt(
        self,
        task_instruction: str,
        rag_context: str,
        error_feedback: Optional[str] = None
    ) -> str:
        """RAG context'i, few-shot örnekleri ve varsa hata geri bildirimini birleştirir."""
        feedback_section = ""
        if error_feedback:
            feedback_section = (
                f"\n### DYNAMIC FEEDBACK (PREVIOUS PLAN FAILED) ###\n"
                f"Error Details: {error_feedback}\n"
                f"Revise the plan to fix this error."
            )

        template = self.prompts.get("user_prompt_template", "")
        return template.format(
            context=rag_context,
            few_shot_examples=self.prompts.get("few_shot_examples", ""),
            task_instruction=task_instruction,
            feedback_section=feedback_section
        )

    def generate_plan(
        self,
        task_instruction: str,
        rag_context: str,
        error_feedback: Optional[str] = None
    ) -> str:
        """
        Doğal dil komutundan Pythonic DSL planı üretir.
        """
        system_prompt = self.prompts.get("system_prompt", "")
        user_prompt = self.build_prompt(task_instruction, rag_context, error_feedback)

        if self.provider == "mock":
            return self._mock_inference(task_instruction, error_feedback)

        if self.provider in ("openai", "ollama"):
            return self._openai_compatible_inference(system_prompt, user_prompt)

        raise ValueError(f"Desteklenmeyen LLM sağlayıcısı: {self.provider}")

    def _openai_compatible_inference(self, system_prompt: str, user_prompt: str) -> str:
        """OpenAI API veya yerel Ollama / vLLM sunucuları ile haberleşir."""
        if OpenAI is None:
            raise ImportError(
                "OpenAI paketi bulunamadı. Kurmak için: "
                "python -m pip install openai"
            )

        api_key = os.getenv(self.api_key_env, "ollama")
        client_kwargs = {"api_key": api_key}
        if self.provider == "ollama":
            client_kwargs["base_url"] = self.base_url

        client = OpenAI(**client_kwargs)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return self._clean_dsl_output(response.choices[0].message.content)

    def _mock_inference(self, task_instruction: str, error_feedback: Optional[str]) -> str:
        """
        GPU veya API anahtarı olmadan uçtan uca pipeline'ı test etmek için
        örnek Pythonic DSL çıktısı döndürür.
        """
        if error_feedback and "closed" in error_feedback.lower():
            return (
                'Robot1.navigate("countertop")\n'
                'Robot1.pickup("apple")\n'
                'Robot1.navigate("fridge")\n'
                'Robot1.open("fridge")\n'
                'Robot1.put("fridge")\n'
                'Robot1.close("fridge")'
            )
        return (
            'Robot1.navigate("countertop")\n'
            'Robot1.pickup("apple")\n'
            'Robot1.navigate("fridge")\n'
            'Robot1.put("fridge")'
        )

    @staticmethod
    def _clean_dsl_output(raw_text: str) -> str:
        """LLM çıktısındaki ```python ... ``` bloklarını temizler."""
        lines = []
        for line in raw_text.strip().splitlines():
            stripped = line.strip()
            if stripped.startswith("```") or not stripped:
                continue
            lines.append(stripped)
        return "\n".join(lines)


# Adım 3 (RAG) + Adım 4 (LLM Planner) Entegrasyon Testi
if __name__ == "__main__":
    print("1. RAG Hafızası (ChromaDB) bağlanıyor...")
    db = VectorDatabaseClient(persist_directory=str(PROJECT_ROOT / "chroma_db"))
    context_builder = ContextBuilder(
        db_client=db,
        wiki_base_dir=str(PROJECT_ROOT / "data/wiki")
    )

    task = "Pick up the apple from the countertop and put it inside the fridge."
    state = "Robot1 is in kitchen. Apple is on countertop. Fridge is closed."

    print("2. Göreve uygun PDDL kuralları RAG'dan çekiliyor...")
    rag_context = context_builder.build_context(task_instruction=task, current_state=state, n_results=3)

    print("3. LLM Planlayıcı başlatılıyor ve Pythonic DSL üretiliyor...\n")
    agent = LLMAgent()
    dsl_plan = agent.generate_plan(task_instruction=task, rag_context=rag_context)

    print("=== ÜRETİLEN PYTHONIC DSL PLANI ===")
    print(dsl_plan)