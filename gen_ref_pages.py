"""Generate the code reference pages and navigation."""

from pathlib import Path
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("jiwer").rglob("*.py")):
    doc_path = path.relative_to("jiwer").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    module_path = path.relative_to("jiwer").with_suffix("")
    parts = list(module_path.parts)

    if parts[-1] == "__init__" or parts[-1] == "cli":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)


with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
