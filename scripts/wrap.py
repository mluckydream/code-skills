#!/usr/bin/env python3
"""
EOD Script - End of Day Workflow

Features:
1. Check uncommitted code status
2. Generate commit message suggestions
3. Collect today's work data
4. Generate work log

Usage:
    python eod.py [--workspace /path/to/project]
"""

import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class EODGenerator:
    """Generate end of day work log"""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.root = workspace_root or Path.cwd()
        self.today = datetime.now().date()
        self.config = self._load_config()
        self.output_base_dir = self.root / self.config.get("workflow", {}).get("output_dir", ".worklogs")
        self.memos_dir_name = self.config.get("workflow", {}).get("memos_dir", "memos")
        self.tasks_dir_name = self.config.get("workflow", {}).get("tasks_dir", "tasks")
        self.worklogs_dir_name = self.config.get("workflow", {}).get("worklogs_dir", "worklogs")

    def _load_config(self) -> dict:
        """Load workflow configuration from multiple possible locations"""
        config_paths = [
            # Project-level
            self.root / ".skills/code-skills/config/skills-config.yaml",
            self.root / "code-skills/config/skills-config.yaml",
            # Claude Code global
            Path.home() / ".claude/CodeSkills/config/skills-config.yaml",
            # Codex CLI global
            Path.home() / ".codex/CodeSkills/config/skills-config.yaml",
            # Relative to script
            Path(__file__).parent.parent / "config/skills-config.yaml",
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, encoding="utf-8") as f:
                        return yaml.safe_load(f) or {}
                except Exception as e:
                    print(f"⚠️ Config load failed: {e}")
        return {}

    def check_git_status(self) -> Dict[str, Any]:
        """Check git status"""
        result = {
            "branch": "unknown",
            "uncommitted": [],
            "unpushed": [],
            "today_commits": [],
            "stats": {"files": 0, "insertions": 0, "deletions": 0},
        }

        try:
            # Current branch
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )
            result["branch"] = branch.stdout.strip()

            # Uncommitted changes
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )
            if status.stdout.strip():
                result["uncommitted"] = status.stdout.strip().split("\n")

            # Unpushed commits
            unpushed = subprocess.run(
                ["git", "log", f"origin/{result['branch']}..HEAD", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )
            if unpushed.stdout.strip():
                result["unpushed"] = unpushed.stdout.strip().split("\n")

            # Today's commits
            today_str = self.today.strftime("%Y-%m-%d")
            commits = subprocess.run(
                ["git", "log", f"--since={today_str} 00:00", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )
            if commits.stdout.strip():
                result["today_commits"] = commits.stdout.strip().split("\n")

            # Stats
            diff_stat = subprocess.run(
                ["git", "diff", "--stat", f"--since={today_str} 00:00", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )
            # Parse stats from output
            for line in diff_stat.stdout.split("\n"):
                if "file" in line and "changed" in line:
                    parts = line.split(",")
                    for part in parts:
                        if "file" in part:
                            result["stats"]["files"] = int(
                                "".join(filter(str.isdigit, part)) or 0
                            )
                        elif "insertion" in part:
                            result["stats"]["insertions"] = int(
                                "".join(filter(str.isdigit, part)) or 0
                            )
                        elif "deletion" in part:
                            result["stats"]["deletions"] = int(
                                "".join(filter(str.isdigit, part)) or 0
                            )

        except Exception as e:
            print(f"⚠️ Git error: {e}")

        return result

    def suggest_commit_message(self) -> Optional[str]:
        """Suggest commit message based on changes"""
        try:
            diff = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )

            if not diff.stdout.strip():
                diff = subprocess.run(
                    ["git", "diff", "--stat"],
                    capture_output=True,
                    text=True,
                    cwd=self.root,
                )

            if not diff.stdout.strip():
                return None

            # Simple heuristic for commit type
            files = diff.stdout.lower()
            if "test" in files:
                return "test: add/update tests"
            elif "readme" in files or "doc" in files:
                return "docs: update documentation"
            elif "fix" in files:
                return "fix: bug fixes"
            else:
                return "feat: implement changes"

        except Exception:
            return None

    def collect_memos(self) -> List[str]:
        """Collect today's memos"""
        memos = []
        memo_file = (
            self.output_base_dir
            / self.memos_dir_name
            / f"{self.today.year}-{self.today.month:02d}/{self.today.day:02d}.md"
        )

        if memo_file.exists():
            try:
                content = memo_file.read_text(encoding="utf-8")
                # Extract memo entries
                for line in content.split("\n"):
                    if line.startswith("- "):
                        memos.append(line[2:])
            except Exception:
                pass

        return memos

    def scan_completed_tasks(self) -> List[dict]:
        """Scan today's completed tasks"""
        completed = []
        tasks_dir = self.output_base_dir / self.tasks_dir_name / "active"

        if not tasks_dir.exists():
            return completed

        for md_file in tasks_dir.rglob("*.md"):
            if md_file.name == "README.md":
                continue

            try:
                content = md_file.read_text(encoding="utf-8")
                if not content.startswith("---"):
                    continue

                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue

                metadata = yaml.safe_load(parts[1])
                if not metadata:
                    continue

                if metadata.get("status") == "done":
                    updated = metadata.get("updated")
                    if updated:
                        if hasattr(updated, "date"):
                            updated = updated.date()
                        elif isinstance(updated, str):
                            updated = datetime.strptime(updated, "%Y-%m-%d").date()

                        if updated == self.today:
                            completed.append(metadata)

            except Exception:
                pass

        return completed

    def scan_in_progress_tasks(self) -> List[dict]:
        """Scan in-progress tasks"""
        in_progress = []
        tasks_dir = self.output_base_dir / self.tasks_dir_name / "active"

        if not tasks_dir.exists():
            return in_progress

        for md_file in tasks_dir.rglob("*.md"):
            if md_file.name == "README.md":
                continue

            try:
                content = md_file.read_text(encoding="utf-8")
                if not content.startswith("---"):
                    continue

                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue

                metadata = yaml.safe_load(parts[1])
                if metadata and metadata.get("status") == "in-progress":
                    in_progress.append(metadata)

            except Exception:
                pass

        return in_progress

    def generate_worklog(
        self,
        git_status: Dict[str, Any],
        completed_tasks: List[dict],
        in_progress_tasks: List[dict],
        memos: List[str],
    ) -> str:
        """Generate work log content"""
        date_str = self.today.strftime("%Y-%m-%d")
        weekday = self.today.strftime("%A")

        lines = [
            f"# Work Log - {date_str} {weekday}",
            "",
            "## 📊 Stats",
            "",
            f"- Commits: {len(git_status.get('today_commits', []))}",
            f"- Files changed: {git_status['stats']['files']}",
            f"- Lines: +{git_status['stats']['insertions']} / -{git_status['stats']['deletions']}",
            "",
        ]

        # Today's commits
        if git_status.get("today_commits"):
            lines.extend([
                "## 📝 Commits",
                "",
            ])
            for commit in git_status["today_commits"]:
                lines.append(f"- {commit}")
            lines.append("")

        # Completed tasks
        if completed_tasks:
            lines.extend([
                "## ✅ Completed",
                "",
            ])
            for task in completed_tasks:
                lines.append(f"- [{task.get('id')}] {task.get('title')}")
            lines.append("")

        # In progress
        if in_progress_tasks:
            lines.extend([
                "## 🔄 In Progress",
                "",
            ])
            for task in in_progress_tasks:
                progress = task.get("progress", "")
                progress_str = f" ({progress}%)" if progress else ""
                lines.append(f"- [{task.get('id')}] {task.get('title')}{progress_str}")
            lines.append("")

        # Memos
        if memos:
            lines.extend([
                "## 📌 Notes",
                "",
            ])
            for memo in memos:
                lines.append(f"- {memo}")
            lines.append("")

        # Footer
        lines.extend([
            "---",
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        ])

        return "\n".join(lines)

    def save_worklog(self, content: str) -> Path:
        """Save work log"""
        year, week, _ = self.today.isocalendar()
        week_dir = self.output_base_dir / self.worklogs_dir_name / f"{year}-W{week:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)

        day_str = f"{self.today.month:02d}-{self.today.day:02d}"
        log_path = week_dir / f"{day_str}.md"

        with open(log_path, "w", encoding="utf-8") as f:
            f.write(content)

        return log_path

    def run(self) -> None:
        """Run the EOD workflow"""
        print(f"✅【CodeSkills】- End of Day ({self.today.strftime('%Y-%m-%d')})")
        print()

        # Git status
        print("📋 Code Status:")
        git_status = self.check_git_status()
        print(f"  - Branch: {git_status['branch']}")

        if git_status["uncommitted"]:
            print(f"  - ⚠️ Uncommitted: {len(git_status['uncommitted'])} files")
        else:
            print("  - ✓ All committed")

        if git_status["unpushed"]:
            print(f"  - ⚠️ Unpushed: {len(git_status['unpushed'])} commits")
        print()

        # Stats
        print("📊 Today's Stats:")
        print(f"  - Commits: {len(git_status.get('today_commits', []))}")
        print(f"  - Files: {git_status['stats']['files']}")
        print(
            f"  - Lines: +{git_status['stats']['insertions']} / -{git_status['stats']['deletions']}"
        )
        print()

        # Suggest commit if needed
        if git_status["uncommitted"]:
            suggestion = self.suggest_commit_message()
            if suggestion:
                print(f"💡 Suggested commit: {suggestion}")
                print()

        # Collect data
        completed = self.scan_completed_tasks()
        in_progress = self.scan_in_progress_tasks()
        memos = self.collect_memos()

        if completed:
            print(f"✅ Completed ({len(completed)}):")
            for task in completed:
                print(f"  - [{task.get('id')}] {task.get('title')}")
            print()

        if in_progress:
            print(f"🔄 In Progress ({len(in_progress)}):")
            for task in in_progress:
                print(f"  - [{task.get('id')}] {task.get('title')}")
            print()

        # Generate and save
        content = self.generate_worklog(git_status, completed, in_progress, memos)
        log_path = self.save_worklog(content)

        print("────")
        print(f"📝 Work log generated: {log_path.relative_to(self.root)}")

        if git_status["unpushed"]:
            print("🔄 Next: Consider running `git push`")


def main():
    parser = argparse.ArgumentParser(description="Generate end of day work log")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace root path",
    )
    args = parser.parse_args()

    generator = EODGenerator(workspace_root=args.workspace)
    generator.run()


if __name__ == "__main__":
    main()
