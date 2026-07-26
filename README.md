# NEXUS CORE v2

Système multi-agent LangGraph pour piloter le cycle de vie de produits SaaS, logiciels,
sites avancés, IA, WordPress et Readymag/ReadyAI.

## Agents

- **AURA** — PRD, roadmap et architecture fonctionnelle
- **PIXEL** — UX, composants et design system Figma
- **ARTISAN** — direction artistique et génération d'assets
- **WEAVER** — WordPress, ReadyAI et Readymag
- **FORGE** — architecture, backend, données et exécution sandboxée
- **ECHO** — contenu, SEO et growth
- **CYPHER** — orchestration, audit sécurité et go/no-go
- **ATELIER** — direction artistique, vulgarisation et édition HTML/PDF/Word

Le routage est adapté à la cible. Un projet web passe par les sept agents; un projet IA
saute les étapes Figma/CMS qui ne sont pas utiles. Les livrables sont écrits dans
`artifacts/<nom-du-projet>/`.

ATELIER intervient après l'audit CYPHER. Pour un projet nommé exactement
`Autocommerce`, il produit automatiquement quatre rapports exécutifs : analyse
fonctionnelle, benchmark marché, méthodologie appliquée, et spécifications MVP
Figma/Make. Chaque rapport inclut une couverture, un sommaire, la signature imposée,
des styles pour tableaux/callouts et un export HTML/PDF/Word éditable dans
`artifacts/Autocommerce/executive-documents/`.

Les projets indépendants peuvent être exécutés en parallèle avec
`NexusOrchestrator.run_many(...)`. La concurrence est bornée par
`NEXUS_MAX_PARALLEL_PROJECTS` afin de maîtriser les coûts et les limites API.

## Installation

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Renseignez au minimum `OPENAI_API_KEY`. Les autres intégrations sont optionnelles tant
qu'elles ne sont pas appelées. Le mode sûr `NEXUS_DRY_RUN=true` est activé par défaut.

## Exécution

```bash
python main.py validate-config
python main.py run \
  --name "Acme Cloud" \
  --target saas \
  --brief "Plateforme B2B de suivi énergétique avec espaces multi-tenant."
```

Pour WordPress :

```bash
python main.py run \
  --name "Acme Editorial" \
  --target wordpress \
  --brief "Refonte du hub éditorial avec CPT études de cas et optimisation SEO."
```

`--publish` exprime une autorisation fonctionnelle, mais ne désactive pas le garde-fou.
Il faut également définir `NEXUS_DRY_RUN=false`. Les connecteurs ne sont pas appelés
automatiquement par le graphe : ils constituent une couche d'intégration explicite à
brancher après validation humaine, afin d'éviter toute mutation externe involontaire.

## Connecteurs

- `tools/figma_tool.py` : lecture Figma REST et pont vers un plugin Figma
- `tools/adobe_tool.py` : génération Firefly
- `tools/wordpress_tool.py` : posts/pages/CPT via WordPress REST
- `tools/readyai_tool.py` : webhooks idempotents ReadyAI/Readymag
- `tools/code_runner_tool.py` : Python/Node dans une racine restreinte

> Le runner local réduit la surface d'exécution mais n'est pas une frontière de sécurité
> forte. En production, remplacez-le par des conteneurs éphémères sans réseau, non-root,
> avec limites CPU/mémoire et filesystem en lecture seule.

## Validation

```bash
pytest
ruff check .
```

## Sécurité

- secrets uniquement via `.env`/variables d'environnement, jamais dans les logs;
- mutations désactivées par défaut;
- timeouts, retries bornés et erreurs HTTP normalisées;
- WordPress publie en brouillon en dry-run;
- webhooks avec clé d'idempotence;
- chemins du runner vérifiés contre `SANDBOX_ROOT`;
- redirections HTTP désactivées pour limiter les risques SSRF.

## Politique GitHub et confidentialité

- Un dépôt privé distinct est utilisé pour chaque projet.
- Le code, les automatisations, les données client et les livrables sensibles restent privés.
- Les fichiers `.env`, environnements locaux, caches et outils téléchargés ne sont jamais versionnés.
- Les contenus destinés au portfolio sont préparés séparément et expurgés de toute information
  confidentielle.
- Un dépôt ou livrable ne devient public qu'après l'autorisation explicite de DJIBI DJIGO.
- L'identité Git principale du projet est `DJIGO DJIBI <uxuidjibi@gmail.com>`.
