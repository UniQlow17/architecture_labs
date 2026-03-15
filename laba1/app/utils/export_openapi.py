import json
from pathlib import Path

import yaml

from app.main import app

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "docs"


def export_openapi() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    schema = app.openapi()

    json_path = DOCS_DIR / "openapi.json"
    json_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported: {json_path}")

    yaml_path = DOCS_DIR / "openapi.yaml"
    yaml_path.write_text(
        yaml.dump(schema, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Exported: {yaml_path}")


if __name__ == "__main__":
    export_openapi()
