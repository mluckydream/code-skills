#!/usr/bin/env python3
"""
Today Script - Daily Task Summary Generator

Features:
1. Switch to main branch and pull latest code
2. Scan task files for YAML metadata
3. Categorize and summarize today's tasks
4. Generate today.md file

Usage:
    python today.py [--workspace /path/to/project] [--skip-sync]
"""

import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class TodayGenerator:
    """Generate daily task summary"""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.root = workspace_root or Path.cwd()
        self.today = datetime.now().date()
        self.config = self._load_config()
        self.output_base_dir = self.root / self.config.get("workflow", {}).get("output_dir", ".worklogs")
        self.tasks_dir_name = self.config.get("workflow", {}).get("tasks_dir", "tasks")
        self.worklogs_dir_name = self.config.get("workflow", {}).get("worklogs_dir", "worklogs")

    def _load_config(self) -> dict:
        """Load workflow configuration from multiple possible locations"""
        # Try multiple config paths (project-level, global, etc.)
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

    def sync_git(self, skip_sync: bool = False) -> Dict[str, Any]:
        """Sync with remote repository"""
        result = {
            "success": False,
            "branch": "unknown",
            "latest_commit": "",
            "message": "",
        }
        
        if skip_sync:
            result["message"] = "Git sync skipped"
            result["success"] = True
            try:
                branch = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True,
                    cwd=self.root,
                )
                result["branch"] = branch.stdout.strip() or "unknown"
            except Exception:
                pass
            return result

        try:
            # Check for uncommitted changes
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )

            if status.stdout.strip():
                result["message"] = "Uncommitted changes detected. Please stash or commit first."
                result["success"] = False
                return result

            # Fetch all
            subprocess.run(
                ["git", "fetch", "--all"],
                capture_output=True,
                cwd=self.root,
                timeout=30,
            )

            # Get current branch
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )
            result["branch"] = branch.stdout.strip()

            # Pull latest
            pull = subprocess.run(
                ["git", "pull", "origin", result["branch"]],
                capture_output=True,
                text=True,
                cwd=self.root,
                timeout=60,
            )

            # Get latest commit
            log = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%h %s"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )
            result["latest_commit"] = log.stdout.strip()
            result["success"] = True
            result["message"] = "Sync completed"

        except subprocess.TimeoutExpired:
            result["message"] = "Git operation timed out"
        except Exception as e:
            result["message"] = f"Git error: {str(e)}"

        return result

    def scan_tasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scan task files and extract metadata"""
        tasks = {
            "today": [],
            "upcoming": [],
            "in-progress": [],
            "overdue": [],
            "long-term": [],
        }
        
        scan_dirs_config = self.config.get("skills", {}).get("today", {}).get("scan_dirs", [])
        
        for relative_dir in scan_dirs_config:
            full_scan_dir = self.output_base_dir / relative_dir
            if not full_scan_dir.exists():
                continue
            
            for md_file in full_scan_dir.rglob("*.md"):
                if md_file.name == "README.md":
                    continue
                
                task_data = self._parse_task(md_file)
                if task_data:
                    self._categorize_task(task_data, tasks)
        return tasks

    def _parse_task(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse task file and extract YAML frontmatter"""
        try:
            content = file_path.read_text(encoding="utf-8")
            if not content.startswith("---"):
                return None

            parts = content.split("---", 2)
            if len(parts) < 3:
                return None

            metadata = yaml.safe_load(parts[1])
            if not metadata or metadata.get("type") != "task":
                return None

            metadata["_file"] = file_path
            return metadata

        except Exception:
            return None

    def _categorize_task(
        self, task: Dict[str, Any], categories: Dict[str, List]
    ) -> None:
        """Categorize task based on status and dates"""
        status = task.get("status", "todo")
        due = task.get("due")
        expected = task.get("expected")

        # Skip completed tasks
        if status == "done":
            return

        # In progress
        if status == "in-progress":
            categories["in-progress"].append(task)
            return

        # Parse dates
        due_date = self._parse_date(due)
        expected_date = self._parse_date(expected)

        # Today
        if due_date == self.today:
            categories["today"].append(task)
        # Overdue
        elif due_date and due_date < self.today:
            categories["overdue"].append(task)
        # Upcoming (within 7 days)
        elif due_date and due_date <= self.today + timedelta(days=7):
            categories["upcoming"].append(task)
        elif expected_date and expected_date <= self.today + timedelta(days=7):
            categories["upcoming"].append(task)
        # Long-term
        else:
            categories["long-term"].append(task)

    def _parse_date(self, date_value: Any) -> Optional[datetime]:
        """Parse date from various formats"""
        if not date_value:
            return None
        if isinstance(date_value, datetime):
            return date_value.date()
        if hasattr(date_value, "date"):
            return date_value
        try:
            return datetime.strptime(str(date_value), "%Y-%m-%d").date()
        except ValueError:
            return None

    def generate_today_md(
        self, git_result: Dict[str, Any], tasks: Dict[str, List]
    ) -> str:
        """Generate today.md content"""
        weekday = self.today.strftime("%A")
        date_str = self.today.strftime("%Y-%m-%d")

        lines = [
            f"# Today - {date_str} {weekday}",
            "",
            "## 📌 Git Status",
            "",
        ]

        # Git status
        if git_result.get("success"):
            lines.extend([
                f"- Branch: `{git_result.get('branch', 'unknown')}`",
                f"- Latest: `{git_result.get('latest_commit', 'N/A')}`",
            ])
        else:
            lines.append(f"- ⚠️ {git_result.get('message', 'Sync failed')}")

        lines.append("")

        # Task sections
        section_config = [
            ("🔴 Today", "today", "□"),
            ("🟡 In Progress", "in-progress", "◐"),
            ("⚠️ Overdue", "overdue", "⚡"),
            ("📅 This Week", "upcoming", "○"),
            ("📋 Long-term", "long-term", "○"),
        ]

        for title, key, icon in section_config:
            task_list = tasks.get(key, [])
            if task_list:
                lines.extend([
                    f"## {title} ({len(task_list)})",
                    "",
                ])
                for task in task_list:
                    task_id = task.get("id", "???")
                    task_title = task.get("title", "Untitled")
                    priority = task.get("priority", "P2")
                    assignee = task.get("assignee", "")
                    assignee_str = f" @{assignee}" if assignee else ""
                    lines.append(f"- {icon} [{task_id}] {task_title} - {priority}{assignee_str}")
                lines.append("")

        # Footer
        lines.extend([
            "---",
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        ])

        return "\n".join(lines)

    def save_today_md(self, content: str) -> Path:
        """Save today.md file"""
        year, week, _ = self.today.isocalendar()
        week_dir = self.output_base_dir / self.worklogs_dir_name / f"{year}-W{week:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)

        log_path = week_dir / "today.md"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(content)
        return log_path

    def run(self, skip_sync: bool = False) -> None:
        """Run the today workflow"""
        print(f"✅【CodeSkills】- Today ({self.today.strftime('%Y-%m-%d %A')})")
        print()

        # Git sync
        print("📌 Git Sync:")
        git_result = self.sync_git(skip_sync=skip_sync)
        if git_result.get("success"):
            print(f"  - Branch: {git_result.get('branch', 'unknown')}")
            if git_result.get("latest_commit"):
                print(f"  - Latest: {git_result.get('latest_commit')}")
            if git_result.get("message"):
                print(f"  - {git_result.get('message')}")
        else:
            print(f"  - ⚠️ {git_result.get('message', 'Failed')}")
        print()

        # Scan tasks
        tasks = self.scan_tasks()

        # Display tasks
        section_config = [
            ("🔴 Today", "today"),
            ("🟡 In Progress", "in-progress"),
            ("⚠️ Overdue", "overdue"),
            ("📅 This Week", "upcoming"),
        ]

        for title, key in section_config:
            task_list = tasks.get(key, [])
            if task_list:
                print(f"{title} ({len(task_list)}):")
                for task in task_list:
                    task_id = task.get("id", "???")
                    task_title = task.get("title", "Untitled")
                    print(f"  - [{task_id}] {task_title}")
                print()

        # Generate and save
        content = self.generate_today_md(git_result, tasks)
        log_path = self.save_today_md(content)

        print("────")
        print(f"📝 today.md generated: {log_path.relative_to(self.root)}")
        print("🔄 Next: Use /task to manage tasks, or start working")


def main():
    parser = argparse.ArgumentParser(description="Generate daily task summary")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace root path",
    )
    parser.add_argument(
        "--skip-sync",
        action="store_true",
        help="Skip git sync step",
    )
    args = parser.parse_args()

    generator = TodayGenerator(workspace_root=args.workspace)
    generator.run(skip_sync=args.skip_sync)


if __name__ == "__main__":
    main()
