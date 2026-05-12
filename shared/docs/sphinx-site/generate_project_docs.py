#!/usr/bin/env python3
"""
Automatic project discovery and documentation generator for Sphinx site.
Recursively scans the repository for README files and generates MyST Markdown pages.
"""

import os
import re
from pathlib import Path


# Directory names to skip during recursive discovery
IGNORED_DIR_NAMES = {
    ".git", "venv", ".venv", "node_modules", "__pycache__",
    ".pytest_cache", "build", "dist", ".tox", ".mypy_cache",
    "site-packages", "htmlcov", ".eggs", ".vscode", ".idea",
    # Standard project structure dirs — documented via the project's own README
    "src", "tests", "docs", "data",
}

# Top-level category directories to scan
TOP_LEVEL_CATEGORIES = [
    "python", "csharp", "frontend", "machine-learning",
    "fullstack-projects", "experiments",
]

_DISPLAY_NAMES: dict[str, str] = {
    "machine-learning": "Machine Learning",
    "python_web-frameworks": "Python Web Frameworks",
    "python_automation-testing": "Python Automation Testing",
    "csharp": "C# Projects",
    "csharp_console-apps": "C# Console Apps",
    "csharp_desktop-apps": "C# Desktop Apps",
    "csharp_desktop-apps_wpf": "C# WPF Desktop Apps",
    "csharp_web-development": "C# Web Development",
    "frontend_react": "React Projects",
    "frontend_vue": "Vue.js Projects",
    "fullstack-projects": "Full-Stack Projects",
}


# ---------------------------------------------------------------------------
# Content helpers
# ---------------------------------------------------------------------------

def get_readme_content_without_h1(readme_path: Path) -> str:
    """Return README content with the first H1 header stripped."""
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if lines and lines[0].startswith("# "):
        return "".join(lines[1:]).lstrip()
    return "".join(lines)


def create_title_from_readme(readme_path: Path) -> str:
    """Extract the first H1 heading from a README, falling back to directory name."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        if first_line.startswith("#"):
            return first_line.lstrip("# ")
        return readme_path.parent.name.replace("-", " ").title()
    except Exception:
        return readme_path.parent.name.replace("-", " ").title()


def extract_project_description(readme_path: Path) -> str:
    """Return the first non-heading, non-code paragraph from a README."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("```"):
                if len(line) > 300:
                    for end_char in (".", "!", "?"):
                        pos = line.find(end_char, 100, 250)
                        if pos != -1:
                            return line[: pos + 1]
                    words = line[:250].split()
                    return " ".join(words[:-1]) + "..."
                return line

        return "A project showcasing development skills and best practices."
    except Exception:
        return "A project showcasing development skills and best practices."


def extract_project_technologies(readme_path: Path) -> list[str]:
    """Extract and deduplicate technologies mentioned in a README."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        tech_patterns = {
            "fastapi": ("FastAPI", 10),
            "django": ("Django", 10),
            "flask": ("Flask", 10),
            "react": ("React", 10),
            "vue": ("Vue.js", 10),
            "angular": ("Angular", 10),
            "typescript": ("TypeScript", 8),
            "javascript": ("JavaScript", 8),
            "python": ("Python", 8),
            "c#": ("C#", 8),
            "aspnet": ("ASP.NET", 9),
            "blazor": ("Blazor", 9),
            "wpf": ("WPF", 9),
            "maui": ("MAUI", 9),
            ".net": (".NET", 8),
            "pytorch": ("PyTorch", 9),
            "tensorflow": ("TensorFlow", 9),
            "scikit-learn": ("Scikit-learn", 9),
            "monai": ("MONAI", 9),
            "pandas": ("Pandas", 8),
            "numpy": ("NumPy", 8),
            "docker": ("Docker", 7),
            "kubernetes": ("Kubernetes", 7),
            "postgresql": ("PostgreSQL", 7),
            "mongodb": ("MongoDB", 7),
            "redis": ("Redis", 7),
            "sqlite": ("SQLite", 7),
            "pywinauto": ("PyWinAuto", 10),
            "ui automation": ("UI Automation", 9),
            "performance testing": ("Performance Testing", 9),
            "pytest": ("PyTest", 8),
            "selenium": ("Selenium", 8),
            "test automation": ("Test Automation", 7),
            "automation": ("Automation", 6),
            "testing": ("Testing", 5),
        }

        found: dict[str, int] = {}
        for pattern, (display, priority) in tech_patterns.items():
            if pattern in content:
                if display not in found or found[display] < priority:
                    found[display] = priority

        final = set(found.keys())
        if any(t in final for t in ("PyTest", "Performance Testing", "UI Automation", "Test Automation")):
            final.discard("Testing")
        if any(t in final for t in ("Test Automation", "UI Automation")):
            final.discard("Automation")

        return sorted(final)
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def find_all_project_readmes(root_path: Path) -> list[dict]:
    """
    Recursively discover all project README files under the top-level category dirs.

    Each README at path  <category>/<...intermediates...>/<project>/README.md
    is represented as a dict with:
      - name         : project directory name
      - category     : underscore-joined path up to (not including) the project dir,
                       prefixed by the top-level category name
                       e.g. 'machine-learning' or 'python_web-frameworks'
      - cat_parts    : list of path segments that make up the category
                       e.g. ['machine-learning'] or ['python', 'web-frameworks']
      - depth        : number of directory levels from category root to project
      - slug         : snake_case project name for page filename generation
      - path         : relative path from source/projects/ to the README (for include)
      - full_path    : absolute Path to the README
      - title        : first H1 heading (or directory name)
      - description  : first description paragraph
      - technologies : list of detected technologies
    """
    sphinx_projects_dir = root_path / "shared/docs/sphinx-site/source/projects"
    readmes: list[dict] = []

    for category_name in TOP_LEVEL_CATEGORIES:
        cat_path = root_path / category_name
        if not cat_path.exists():
            continue

        for readme_path in sorted(cat_path.rglob("README.md")):
            # Parts relative to the category root, e.g. ('pyhealth', 'README.md')
            relative = readme_path.relative_to(cat_path)
            parts = relative.parts

            # Skip if any directory component is an infrastructure dir
            if any(part in IGNORED_DIR_NAMES for part in parts[:-1]):
                continue

            # Skip the top-level category README itself (e.g. machine-learning/README.md)
            if len(parts) == 1:
                continue

            # project_parts = directory path from category root to the project (no README.md)
            project_parts = parts[:-1]
            project_name = project_parts[-1]

            if len(project_parts) == 1:
                # Direct child: machine-learning/pyhealth
                category = category_name
                cat_parts = [category_name]
            else:
                # Nested: python/web-frameworks/fastapi
                intermediate = "_".join(project_parts[:-1])
                category = f"{category_name}_{intermediate}"
                cat_parts = [category_name] + list(project_parts[:-1])

            slug = project_name.lower().replace("-", "_").replace(" ", "_")
            rel_path = os.path.relpath(readme_path, sphinx_projects_dir).replace("\\", "/")

            readmes.append({
                "name": project_name,
                "category": category,
                "cat_parts": cat_parts,
                "depth": len(project_parts),
                "path": rel_path,
                "full_path": readme_path,
                "title": create_title_from_readme(readme_path),
                "description": extract_project_description(readme_path),
                "technologies": extract_project_technologies(readme_path),
                "slug": slug,
            })

    print(f"Discovered {len(readmes)} README files across top-level category dirs")
    return readmes


def _build_cat_parts_map(readmes: list[dict]) -> dict[str, list[str]]:
    """Map each unique category name to its cat_parts list."""
    result: dict[str, list[str]] = {}
    for readme in readmes:
        result.setdefault(readme["category"], readme["cat_parts"])
    return result


def _direct_sub_categories(category: str, cat_parts_map: dict[str, list[str]]) -> list[str]:
    """Return category names that are exactly one level deeper than the given category."""
    parent_parts = cat_parts_map.get(category, [])
    parent_depth = len(parent_parts)
    direct_subs = {
        cat for cat, parts in cat_parts_map.items()
        if len(parts) == parent_depth + 1 and parts[:parent_depth] == parent_parts
    }
    return sorted(direct_subs)


# ---------------------------------------------------------------------------
# MyST Markdown block builders
# ---------------------------------------------------------------------------

def _toctree_block(entries: list[str], maxdepth: int = 1, hidden: bool = True) -> str:
    """Generate a MyST toctree directive block."""
    opts = ":maxdepth: " + str(maxdepth) + "\n"
    if hidden:
        opts += ":hidden:\n"
    return "```{toctree}\n" + opts + "\n" + "\n".join(entries) + "\n```"


def _include_block(path: str) -> str:
    """Generate a MyST include directive block."""
    return "```{include} " + path + "\n```"


def _admonition_block(title: str, body: str, cls: str = "tip") -> str:
    """Generate a MyST admonition directive block."""
    return "```{admonition} " + title + "\n:class: " + cls + "\n\n" + body + "\n```"


def _project_grid(projects: list[dict]) -> str:
    """
    MyST colon-fence grid of project cards with button-ref links.
    Nesting: :::::{grid} > ::::{grid-item-card} > :::{button-ref}
    """
    lines = [":::::{grid} 1 2 2 2", ":gutter: 3", ":margin: 2", ""]
    for p in sorted(projects, key=lambda x: x["title"]):
        slug = p["category"] + "_" + p["slug"]
        tech_line = ""
        if p["technologies"]:
            tech_line = "\n\n" + " ".join(
                "{bdg-secondary}`" + t + "`" for t in p["technologies"]
            )
        lines.append("::::{grid-item-card} " + p["title"])
        lines.append(":link: " + slug)
        lines.append(":link-type: doc")
        lines.append(":class-card: project-card")
        lines.append(":text-align: left")
        lines.append("")
        lines.append(p["description"] + tech_line)
        lines.append("")
        lines.append("+++")
        lines.append("")
        lines.append(":::{button-ref} " + slug)
        lines.append(":color: primary")
        lines.append(":outline:")
        lines.append(":expand:")
        lines.append(":ref-type: doc")
        lines.append("")
        lines.append("View Details")
        lines.append(":::")
        lines.append("::::")
        lines.append("")
    lines.append(":::::")
    return "\n".join(lines)


def _subcategory_grid(categories: list[str]) -> str:
    """
    MyST colon-fence grid of sub-category cards.
    Nesting: ::::{grid} > :::{grid-item-card}
    """
    lines = ["::::{grid} 1 2 2 2", ":gutter: 3", ":margin: 2", ""]
    for cat in sorted(categories):
        name = _DISPLAY_NAMES.get(cat, cat.replace("_", " ").replace("-", " ").title())
        lines.append(":::{grid-item-card} " + name)
        lines.append(":link: " + cat)
        lines.append(":link-type: doc")
        lines.append(":class-card: category-card")
        lines.append(":text-align: center")
        lines.append("")
        lines.append("Explore sub-projects")
        lines.append("")
        lines.append("+++")
        lines.append("Explore")
        lines.append(":::")
        lines.append("")
    lines.append("::::")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Page generation
# ---------------------------------------------------------------------------

def _clean_generated_pages(output_dir: Path, keep: set[str] | None = None) -> None:
    """Remove all auto-generated RST and MD files, preserving those in the keep set."""
    preserved = keep or {"index.rst"}
    removed = 0
    for ext in ("*.rst", "*.md"):
        for file in output_dir.glob(ext):
            if file.name not in preserved:
                file.unlink()
                removed += 1
    if removed:
        print(f"Removed {removed} stale generated file(s)")


def generate_project_pages(readmes: list[dict], output_dir: Path) -> None:
    """Generate individual project pages and category overview pages as MyST Markdown files."""

    _clean_generated_pages(output_dir)

    categories: dict[str, list[dict]] = {}
    for readme in readmes:
        categories.setdefault(readme["category"], []).append(readme)

    cat_parts_map = _build_cat_parts_map(readmes)
    category_set = set(categories.keys())

    # Individual project pages
    # Skip any whose slug collides with a category name — those get a merged page below.
    for readme in readmes:
        project_slug = readme["category"] + "_" + readme["slug"]
        if project_slug in category_set:
            continue

        project_file = output_dir / (project_slug + ".md")

        tech_line = ""
        if readme["technologies"]:
            tech_line = "\n**Technologies:** " + " • ".join(readme["technologies"]) + "\n"

        back_label = (
            _DISPLAY_NAMES.get(readme["category"])
            or readme["category"].replace("_", " ").replace("-", " ").title()
        )

        # A project page may itself be the parent of sub-categories.
        child_cats = sorted(cat for cat in categories if cat.startswith(project_slug + "_"))

        parts = [
            "# " + readme["title"],
            "",
            readme["description"],
            tech_line,
            "",
            _include_block(readme["path"]),
        ]

        if child_cats:
            parts += ["", _toctree_block(child_cats), "", "## Sub-Projects", "", _subcategory_grid(child_cats)]

        parts += ["", "---", "", "[← Back to " + back_label + "](" + readme["category"] + ".md)", ""]

        with open(project_file, "w", encoding="utf-8") as f:
            f.write("\n".join(parts))
        print(f"Generated project page: {project_file.name}")

    # Build a lookup for merged-page detection.
    # A collision occurs when a category name equals an individual project slug.
    slug_to_readme: dict[str, dict] = {
        r["category"] + "_" + r["slug"]: r for r in readmes
    }

    # Category overview pages
    for category, projects in sorted(categories.items()):
        cat_name = (
            _DISPLAY_NAMES.get(category)
            or category.replace("_", " ").replace("-", " ").title()
        )
        cat_file = output_dir / (category + ".md")
        sub_cats = _direct_sub_categories(category, cat_parts_map)

        # Merged page when this category name is also an individual project slug.
        parent_readme = slug_to_readme.get(category)

        # Toctree: project pages + sub-category pages (deduplicated)
        seen_entries: set[str] = set()
        toctree_entries: list[str] = []
        for slug_entry in [category + "_" + p["slug"] for p in sorted(projects, key=lambda p: p["name"])]:
            if slug_entry not in seen_entries:
                toctree_entries.append(slug_entry)
                seen_entries.add(slug_entry)
        for sub_cat in sub_cats:
            if sub_cat not in seen_entries:
                toctree_entries.append(sub_cat)
                seen_entries.add(sub_cat)

        if parent_readme:
            # Merged page: README content + sub-project navigation
            tech_line = ""
            if parent_readme["technologies"]:
                tech_line = "\n**Technologies:** " + " • ".join(parent_readme["technologies"]) + "\n"

            parts = [
                "# " + parent_readme["title"],
                "",
                parent_readme["description"],
                tech_line,
                "",
                _include_block(parent_readme["path"]),
                "",
            ]
            if projects or sub_cats:
                parts += ["---", ""]
        else:
            parts = [
                "# " + cat_name + " Projects",
                "",
                "This section showcases all " + cat_name.lower() + " projects with their documentation and source code.",
                "",
                _admonition_block(
                    "Navigation Tip",
                    "Click on any project card to view its complete documentation.",
                ),
                "",
            ]

        if toctree_entries:
            parts += [_toctree_block(toctree_entries), ""]

        if projects:
            section = "## Sub-Projects" if parent_readme else "## Projects"
            parts += [section, "", _project_grid(projects), ""]

        if sub_cats:
            parts += ["## Sub-Categories", "", _subcategory_grid(sub_cats), ""]

        with open(cat_file, "w", encoding="utf-8") as f:
            f.write("\n".join(parts))
        print(f"Generated category page: {cat_file.name}")


# ---------------------------------------------------------------------------
# Index updaters
# ---------------------------------------------------------------------------

def _get_navigation_categories(readmes: list[dict]) -> list[str]:
    """
    Compute the top-level navigation entries shown in projects/index.rst.

    If a top-level category dir has any projects at depth 1 (e.g. machine-learning/pyhealth),
    that top-level dir is used as the single nav entry for the whole category.
    Otherwise, the first two cat_parts are used (e.g. python_web-frameworks).

    If the preferred nav entry doesn't correspond to an actual generated category page
    (e.g. no README exists at that intermediate level), fall back to the actual category.
    """
    actual_categories: set[str] = {r["category"] for r in readmes}

    # Which top-level dirs have at least one direct (depth=1) project?
    top_levels_with_direct_projects: set[str] = {
        r["cat_parts"][0] for r in readmes if r["depth"] == 1
    }

    nav_cats: set[str] = set()
    for readme in readmes:
        parts = readme["cat_parts"]
        top = parts[0]

        if top in top_levels_with_direct_projects:
            candidate = top
        else:
            candidate = "_".join(parts[:2]) if len(parts) >= 2 else top

        if candidate in actual_categories:
            nav_cats.add(candidate)
        else:
            nav_cats.add(readme["category"])

    return sorted(nav_cats)


def update_projects_index(readmes: list[dict], projects_index_path: Path) -> None:
    """Update source/projects/index.rst with all auto-discovered navigation entries."""

    with open(projects_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    nav_cats = _get_navigation_categories(readmes)

    toctree_section = "\n\n**Auto-Discovered Projects**\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n"
    toctree_section += ".. toctree::\n   :maxdepth: 2\n   :caption: Technologies & Projects\n   :hidden:\n\n"
    toctree_section += "".join(f"   {cat}\n" for cat in nav_cats)

    toctree_section += "\n\n.. grid:: 1 2 2 3\n   :gutter: 3\n   :margin: 3\n\n"
    for cat in nav_cats:
        display = _DISPLAY_NAMES.get(cat, cat.replace("_", " ").replace("-", " ").title())
        toctree_section += f"""   .. grid-item-card:: {display}
      :link: {cat}
      :link-type: doc
      :text-align: center
      :class-card: category-card

      Explore projects and documentation

      +++

      Explore →

"""

    if "Auto-Discovered Projects" in content:
        pattern = r"\*\*Auto-Discovered Projects\*\*.*?(?=\*\*|\Z)"
        content = re.sub(pattern, toctree_section.strip(), content, flags=re.DOTALL)
    else:
        content += toctree_section

    with open(projects_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated projects index: {len(nav_cats)} navigation entries")


def update_machine_learning_index(readmes: list[dict], ml_index_path: Path) -> None:
    """Update source/machine-learning/index.md with discovered ML projects."""
    ml_projects = [r for r in readmes if r["category"] == "machine-learning"]
    if not ml_projects:
        return

    with open(ml_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build toctree entries pointing into the projects/ directory
    toctree_entries = "\n".join(
        "../projects/machine-learning_" + p["slug"]
        for p in sorted(ml_projects, key=lambda p: p["name"])
    )
    toctree_block = "```{toctree}\n:maxdepth: 2\n:hidden:\n\n" + toctree_entries + "\n```"

    toctree_pattern = r"```\{toctree\}.*?```"
    if re.search(toctree_pattern, content, re.DOTALL):
        content = re.sub(toctree_pattern, toctree_block, content, flags=re.DOTALL)
    else:
        content += "\n\n" + toctree_block

    # Replace the "Featured Projects" section with discovered content
    projects_md = "\n\n## Featured Projects\n\n"
    for project in sorted(ml_projects, key=lambda p: p["title"]):
        slug = "machine-learning_" + project["slug"]
        techs = ", ".join(project["technologies"]) if project["technologies"] else "Various"
        projects_md += "### [" + project["title"] + "](../projects/" + slug + ")\n\n"
        projects_md += project["description"] + "\n\n"
        if project["technologies"]:
            projects_md += "**Technologies:** " + techs + "\n\n"

    featured_pattern = r"\n\n## Featured Projects\n.*"
    if re.search(featured_pattern, content, re.DOTALL):
        content = re.sub(featured_pattern, projects_md.rstrip(), content, flags=re.DOTALL)
    else:
        content += projects_md

    with open(ml_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated ML index with {len(ml_projects)} project(s)")


def update_python_index(readmes: list[dict], python_index_path: Path, python_dir: Path) -> None:
    """Update source/python/index.md with discovered Python projects."""
    python_projects = [r for r in readmes if r["category"].startswith("python_")]
    if not python_projects:
        return

    standalone_projects = []
    has_web_frameworks = False

    for project in python_projects:
        category_base = project["category"].replace("python_", "")
        if "web-frameworks" in category_base:
            has_web_frameworks = True
        else:
            standalone_projects.append(project)
            project_filename = category_base.replace("_", "-")
            project_file = python_dir / (project_filename + ".md")

            tech_line = ""
            if project["technologies"]:
                tech_line = "**Technologies:** " + " • ".join(project["technologies"])

            readme_content = get_readme_content_without_h1(project["full_path"])
            md_content = (
                "# " + project["title"] + "\n\n"
                + project["description"] + "\n\n"
                + tech_line + "\n\n"
                + readme_content.strip() + "\n\n"
                + "---\n\n[← Back to Python Development](index.md)\n"
            )
            with open(project_file, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"Generated python project file: {project_file.name}")

    with open(python_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    toctree_entries: list[str] = []
    seen: set[str] = set()

    if has_web_frameworks and "web-frameworks" not in seen:
        toctree_entries.append("web-frameworks")
        seen.add("web-frameworks")

    for project in standalone_projects:
        filename = project["category"].replace("python_", "").replace("_", "-")
        if filename not in seen:
            toctree_entries.append(filename)
            seen.add(filename)

    toctree_content = "\n".join(toctree_entries)
    replacement = "```{toctree}\n:maxdepth: 1\n:titlesonly:\n\n" + toctree_content + "\n```"
    toctree_pattern = r"```{toctree}\n:maxdepth: 1\n:titlesonly:\n\n(.*?)```"

    if re.search(toctree_pattern, content, re.DOTALL):
        content = re.sub(toctree_pattern, replacement, content, flags=re.DOTALL)
    else:
        content += "\n\n" + replacement

    with open(python_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated Python index: {len(toctree_entries)} main entries")


def update_csharp_index(readmes: list[dict], csharp_index_path: Path) -> None:
    """Update source/csharp/index.md with discovered C# projects."""
    csharp_projects = [r for r in readmes if r["category"].startswith("csharp_")]
    if not csharp_projects:
        return

    with open(csharp_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    toctree_entries = "\n".join(
        "../projects/" + p["category"] + "_" + p["slug"]
        for p in csharp_projects
    )
    replacement = "```{toctree}\n:maxdepth: 2\n:hidden:\n\n" + toctree_entries + "\n```"
    toctree_pattern = r"```{toctree}\n:maxdepth: 2\n:hidden:\n\n(.*?)```"

    if re.search(toctree_pattern, content, re.DOTALL):
        content = re.sub(toctree_pattern, replacement, content, flags=re.DOTALL)
    else:
        content += "\n\n" + replacement

    with open(csharp_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated C# index with {len(csharp_projects)} project(s)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """Discover all project READMEs and generate Sphinx documentation pages."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent.parent
    sphinx_source = script_dir / "source"
    projects_dir = sphinx_source / "projects"

    print(f"Scanning for README files in: {repo_root}")

    readmes = find_all_project_readmes(repo_root)
    print(f"Found {len(readmes)} project README files")

    if not readmes:
        print("No README files found in project directories.")
        return

    generate_project_pages(readmes, projects_dir)
    update_projects_index(readmes, projects_dir / "index.rst")
    update_csharp_index(readmes, sphinx_source / "csharp" / "index.md")
    update_python_index(readmes, sphinx_source / "python" / "index.md", sphinx_source / "python")
    update_machine_learning_index(readmes, sphinx_source / "machine-learning" / "index.md")

    print("\nDocumentation generation complete!")
    print("Run 'python docs.py build' to rebuild the full site.")


if __name__ == "__main__":
    main()
