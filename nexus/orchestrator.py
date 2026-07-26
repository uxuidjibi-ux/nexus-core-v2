from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from agents import ARTISAN, ATELIER, AURA, CYPHER, ECHO, FORGE, PIXEL, WEAVER
from agents.base import AgentProfile
from agents.creative_dir import AUTOCOMMERCE_DOCUMENTS
from nexus.config import Settings
from nexus.document_renderer import ExecutiveDocumentRenderer
from nexus.models import Deliverable, NexusState, ProjectRequest

logger = logging.getLogger(__name__)


class NexusOrchestrator:
    def __init__(self, settings: Settings):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self.settings = settings
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.2,
            timeout=90,
            max_retries=2,
        )
        self.graph = self._build_graph()
        self.document_renderer = ExecutiveDocumentRenderer()

    def _agent_node(self, profile: AgentProfile):
        def invoke(state: NexusState) -> dict[str, Any]:
            previous = state.get("deliverables", [])
            context = json.dumps(previous, ensure_ascii=False, default=str)
            prompt = (
                f"DEMANDE:\n{json.dumps(state['request'], ensure_ascii=False)}\n\n"
                f"LIVRABLES PRÉCÉDENTS:\n{context[-50_000:]}\n\n"
                "Crée ton livrable maintenant. Structure en Markdown, sois concret et concis."
            )
            logger.info("Agent %s running", profile.name)
            response = self.llm.invoke([("system", profile.system_prompt), ("human", prompt)])
            deliverable = Deliverable(
                agent=profile.name,
                title=f"{profile.name} — {profile.role}",
                content=response.content,
            )
            return {
                "current_agent": profile.name,
                "deliverables": [*previous, deliverable.model_dump(mode="json")],
            }

        return invoke

    def _atelier_node(self, state: NexusState) -> dict[str, Any]:
        previous = state.get("deliverables", [])
        context = json.dumps(previous, ensure_ascii=False, default=str)
        request = state["request"]
        is_autocommerce = request.get("name", "").strip().lower() == "autocommerce"
        specifications = (
            AUTOCOMMERCE_DOCUMENTS
            if is_autocommerce
            else (
                (
                    "rapport-executif",
                    f"Rapport exécutif — {request.get('name', 'Projet')}",
                    "Synthétise la stratégie, l'expérience, la création, la technique, "
                    "le go-to-market, les risques et le plan d'action.",
                ),
            )
        )
        deliverables = list(previous)
        for slug, title, scope in specifications:
            prompt = (
                f"DEMANDE:\n{json.dumps(request, ensure_ascii=False)}\n\n"
                f"DOCUMENT À PRODUIRE:\nTitre: {title}\nPérimètre: {scope}\n\n"
                f"LIVRABLES VALIDÉS PAR CYPHER:\n{context[-70_000:]}\n\n"
                "Rédige le corps complet du document selon ta charte. "
                "Ne reproduis pas la couverture ni le sommaire."
            )
            logger.info("Agent ATELIER running document %s", slug)
            response = self.llm.invoke([("system", ATELIER.system_prompt), ("human", prompt)])
            deliverable = Deliverable(
                agent="ATELIER",
                title=title,
                content=response.content,
                metadata={"document_slug": slug, "format": "executive_report"},
            )
            deliverables.append(deliverable.model_dump(mode="json"))
        return {"current_agent": "ATELIER", "deliverables": deliverables}

    def _route_after_aura(self, state: NexusState) -> str:
        target = state["request"].get("target", "saas")
        design_targets = {"saas", "software", "website", "wordpress", "readymag"}
        return "pixel" if target in design_targets else "artisan"

    def _route_after_artisan(self, state: NexusState) -> str:
        target = state["request"].get("target", "saas")
        return "weaver" if target in {"saas", "website", "wordpress", "readymag"} else "forge"

    def _route_after_weaver(self, state: NexusState) -> str:
        return "forge" if state["request"].get("target") in {"saas", "software", "ai"} else "echo"

    def _build_graph(self):
        builder = StateGraph(NexusState)
        for name, profile in (
            ("aura", AURA),
            ("pixel", PIXEL),
            ("artisan", ARTISAN),
            ("weaver", WEAVER),
            ("forge", FORGE),
            ("echo", ECHO),
            ("cypher", CYPHER),
        ):
            builder.add_node(name, self._agent_node(profile))
        builder.add_node("atelier", self._atelier_node)

        builder.add_edge(START, "aura")
        builder.add_conditional_edges(
            "aura", self._route_after_aura, {"pixel": "pixel", "artisan": "artisan"}
        )
        builder.add_edge("pixel", "artisan")
        builder.add_conditional_edges(
            "artisan", self._route_after_artisan, {"weaver": "weaver", "forge": "forge"}
        )
        builder.add_conditional_edges(
            "weaver", self._route_after_weaver, {"forge": "forge", "echo": "echo"}
        )
        builder.add_edge("forge", "echo")
        builder.add_edge("echo", "cypher")
        builder.add_edge("cypher", "atelier")
        builder.add_edge("atelier", END)
        return builder.compile()

    def run(self, request: ProjectRequest) -> NexusState:
        initial: NexusState = {
            "request": request.model_dump(mode="json"),
            "deliverables": [],
            "errors": [],
            "approved": False,
        }
        result = self.graph.invoke(initial)
        self._write_artifacts(request, result)
        return result

    def run_many(self, requests: list[ProjectRequest]) -> dict[str, NexusState]:
        """Execute independent projects concurrently with a strict worker limit."""
        if not requests:
            return {}
        names = [request.name for request in requests]
        if len(names) != len(set(names)):
            raise ValueError("Parallel project names must be unique")
        results: dict[str, NexusState] = {}
        with ThreadPoolExecutor(
            max_workers=min(self.settings.nexus_max_parallel_projects, len(requests))
        ) as executor:
            futures = {executor.submit(self.run, request): request.name for request in requests}
            for future in as_completed(futures):
                results[futures[future]] = future.result()
        return results

    def _write_artifacts(self, request: ProjectRequest, result: NexusState) -> Path:
        safe_name = "".join(
            char if char.isalnum() or char in "-_" else "-" for char in request.name
        )
        output_dir = self.settings.nexus_artifact_dir / safe_name
        output_dir.mkdir(parents=True, exist_ok=True)
        for index, item in enumerate(result.get("deliverables", []), start=1):
            agent = item["agent"].lower()
            slug = item.get("metadata", {}).get("document_slug", agent)
            markdown_path = output_dir / f"{index:02d}-{slug}.md"
            markdown_path.write_text(f"# {item['title']}\n\n{item['content']}\n", encoding="utf-8")
            if item["agent"] == "ATELIER":
                try:
                    self.document_renderer.render(
                        title=item["title"],
                        content=item["content"],
                        output_dir=output_dir / "executive-documents",
                        slug=slug,
                    )
                except Exception as exc:  # Keep Markdown/HTML-independent pipeline recoverable.
                    logger.exception("Document export failed for %s", slug)
                    result.setdefault("errors", []).append(
                        f"ATELIER export failed for {slug}: {type(exc).__name__}"
                    )
        (output_dir / "run.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
        )
        return output_dir
