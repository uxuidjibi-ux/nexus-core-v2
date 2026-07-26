import json

import typer
from rich.console import Console
from rich.panel import Panel

from nexus.config import get_settings
from nexus.logging import configure_logging
from nexus.models import ProjectRequest
from nexus.orchestrator import NexusOrchestrator

app = typer.Typer(help="NEXUS CORE v2 — orchestration multi-agent.")
console = Console()


@app.command()
def run(
    name: str = typer.Option(..., help="Nom du produit"),
    brief: str = typer.Option(..., help="Brief produit"),
    target: str = typer.Option("saas", help="saas|software|website|wordpress|ai|readymag"),
    constraint: list[str] | None = typer.Option(None, "--constraint", "-c"),  # noqa: B008
    publish: bool = typer.Option(False, help="Autorise les étapes de publication configurées"),
) -> None:
    settings = get_settings()
    configure_logging(settings.nexus_log_level)
    request = ProjectRequest(
        name=name,
        brief=brief,
        target=target,
        constraints=constraint or [],
        publish=publish,
    )
    if publish and settings.nexus_dry_run:
        console.print(
            "[yellow]Publication demandée, mais NEXUS_DRY_RUN=true: aucune mutation externe.[/]"
        )
    result = NexusOrchestrator(settings).run(request)
    output_dir = settings.nexus_artifact_dir / _safe_name(name)
    console.print(
        Panel.fit(
            f"{len(result.get('deliverables', []))} livrables générés\n{output_dir.resolve()}",
            title="NEXUS CORE v2",
        )
    )


@app.command()
def validate_config() -> None:
    settings = get_settings()
    checks = {
        "OpenAI": bool(settings.openai_api_key),
        "Figma": bool(settings.figma_token),
        "Adobe": bool(settings.adobe_access_token and settings.adobe_client_id),
        "WordPress": bool(settings.wp_url and settings.wp_user and settings.wp_app_password),
        "ReadyAI": bool(settings.readyai_webhook_url),
    }
    console.print_json(json.dumps(checks))


def _safe_name(name: str) -> str:
    return "".join(char if char.isalnum() or char in "-_" else "-" for char in name)


if __name__ == "__main__":
    app()
