import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "reconcile_tbhrc_reference.py"
spec = importlib.util.spec_from_file_location("reconcile_tbhrc_reference", MODULE_PATH)
reconcile = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(reconcile)


class ReconcileTBHRCReferenceTests(unittest.TestCase):
    def test_router_membership_parity_uses_names_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            router = root / "router.json"
            reference = root / "reference.json"
            router.write_text(json.dumps({"tbhrc/workspace": "x", "tbhrc/folderdesk": "y"}), encoding="utf-8")
            reference.write_text(json.dumps({
                "target": {"owner": "tbhrc"},
                "repositories": [
                    {"name": "workspace", "role": "workspace", "visibility": "private"},
                    {"name": "folderdesk", "role": "portable-architecture", "visibility": "public"},
                ],
            }), encoding="utf-8")
            self.assertEqual(reconcile.router_repositories(router), {"tbhrc/workspace", "tbhrc/folderdesk"})
            self.assertEqual(reconcile.reference_repositories(reference)[1], {"tbhrc/workspace", "tbhrc/folderdesk"})

    def test_verify_skill_links_detects_only_missing_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills = Path(tmp)
            (skills / "alpha").mkdir()
            (skills / "alpha" / "SKILL.md").write_text("# Alpha\n", encoding="utf-8")
            links = [
                {"document": "AGENTS.md", "kind": "tree", "path": "alpha", "url": "u1", "source": "workspace"},
                {"document": "AGENTS.md", "kind": "blob", "path": "alpha/SKILL.md", "url": "u2", "source": "workspace"},
                {"document": "AGENTS.md", "kind": "tree", "path": "missing", "url": "u3", "source": "workspace"},
            ]
            broken = reconcile.verify_skill_links(skills, links)
            self.assertEqual([row["path"] for row in broken], ["missing"])

    def test_material_skill_links_separates_workspace_and_legacy_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "README.md"
            current = "https://github.com/tbhrc/workspace/tree/main/.folderdesk/skills/ecosystem-librarian"
            legacy = "https://github.com/tbhrc/skills/tree/main/ecosystem-librarian"
            doc.write_text(f"[Current]({current}) [Again]({current}) [Legacy]({legacy})\n", encoding="utf-8")
            links, legacy_links = reconcile.material_skill_links((doc,))
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0]["path"], "ecosystem-librarian")
            self.assertEqual(len(legacy_links), 1)
            self.assertEqual(legacy_links[0]["source"], "legacy")


if __name__ == "__main__":
    unittest.main()
