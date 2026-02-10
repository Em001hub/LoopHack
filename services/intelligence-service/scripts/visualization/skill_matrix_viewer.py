"""
Skill Matrix Viewer
Interactive terminal visualization of team skills
"""

import asyncio
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich import box
from loguru import logger
import numpy as np

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.services.skill_service import SkillService
from src.config.database import AsyncSessionLocal


class SkillMatrixViewer:
    """
    Beautiful terminal UI for viewing team skill matrix
    """
    
    def __init__(self):
        self.console = Console()
        self.skill_service = SkillService()
    
    def _get_skill_color(self, proficiency: float) -> str:
        """Get color based on proficiency level"""
        if proficiency >= 0.8:
            return "green"
        elif proficiency >= 0.6:
            return "yellow"
        elif proficiency >= 0.4:
            return "orange"
        else:
            return "red"
    
    def _create_skill_bar(self, proficiency: float, width: int = 20) -> str:
        """Create visual bar for skill proficiency"""
        filled = int(proficiency * width)
        empty = width - filled
        
        color = self._get_skill_color(proficiency)
        
        bar = "█" * filled + "░" * empty
        return f"[{color}]{bar}[/{color}]"
    
    async def display_team_skill_matrix(self, project_id: str):
        """
        Display comprehensive team skill matrix
        """
        self.console.clear()
        
        # Header
        self.console.print(
            Panel.fit(
                f"[bold cyan]🎯 Team Skill Matrix[/bold cyan]\n"
                f"[dim]Project: {project_id}[/dim]",
                border_style="cyan"
            )
        )
        
        self.console.print()
        
        # Fetch skill matrix
        with self.console.status("[bold green]Loading team skills...") as status:
            async with AsyncSessionLocal() as db:
                matrix = await self.skill_service.generate_team_skill_matrix(db, project_id)
        
        # Display team overview
        self._display_team_overview(matrix)
        
        self.console.print()
        
        # Display skill matrix table
        self._display_skill_table(matrix)
        
        self.console.print()
        
        # Display skill gaps
        self._display_skill_gaps(matrix)
        
        self.console.print()
        
        # Display knowledge silos
        self._display_knowledge_silos(matrix)
        
        self.console.print()
        
        # Display recommendations
        self._display_recommendations(matrix)
    
    def _display_team_overview(self, matrix: dict):
        """Display team overview stats"""
        stats_table = Table(show_header=False, box=box.ROUNDED, border_style="blue")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="bold white")
        
        stats_table.add_row("👥 Team Size", str(matrix['team_size']))
        stats_table.add_row("🎯 Total Skills", str(matrix['total_unique_skills']))
        stats_table.add_row("⚠️  Skill Gaps", str(len(matrix['skill_gaps'])))
        stats_table.add_row("🔴 Knowledge Silos", str(len(matrix['knowledge_silos'])))
        
        self.console.print(
            Panel(
                stats_table,
                title="[bold]Team Overview[/bold]",
                border_style="blue"
            )
        )
    
    def _display_skill_table(self, matrix: dict):
        """Display skill matrix as table"""
        # Create main skill table
        skill_table = Table(
            title="[bold cyan]Skill Coverage Matrix[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
            box=box.DOUBLE_EDGE,
            border_style="cyan"
        )
        
        skill_table.add_column("Skill", style="cyan", width=25)
        skill_table.add_column("Coverage", justify="center", width=40)
        skill_table.add_column("Experts", justify="center", width=10)
        
        # Sort skills by coverage
        skill_matrix = matrix['skill_matrix']
        skill_matrix_sorted = sorted(
            skill_matrix,
            key=lambda x: len(x['coverage']),
            reverse=True
        )
        
        for skill_row in skill_matrix_sorted[:20]:  # Top 20 skills
            skill_name = skill_row['skill']
            coverage = skill_row['coverage']
            
            # Count experts
            expert_count = sum(1 for c in coverage if c['proficiency'] >= 0.8)
            
            # Calculate average proficiency
            if coverage:
                avg_proficiency = np.mean([c['proficiency'] for c in coverage])
            else:
                avg_proficiency = 0
            
            # Create visual bar
            coverage_pct = len(coverage) / matrix['team_size']
            bar = self._create_skill_bar(coverage_pct)
            
            # Skill name with color
            skill_color = self._get_skill_color(avg_proficiency)
            skill_display = f"[{skill_color}]{skill_name}[/{skill_color}]"
            
            # Coverage display
            coverage_display = f"{bar} [dim]{len(coverage)}/{matrix['team_size']}[/dim]"
            
            # Experts display
            if expert_count > 0:
                experts_display = f"[green]{expert_count}[/green]"
            else:
                experts_display = f"[red]0[/red]"
            
            skill_table.add_row(skill_display, coverage_display, experts_display)
        
        self.console.print(skill_table)
    
    def _display_skill_gaps(self, matrix: dict):
        """Display skill gaps"""
        if not matrix['skill_gaps']:
            self.console.print("[green]✅ No significant skill gaps detected[/green]")
            return
        
        gaps_table = Table(
            title="[bold yellow]⚠️  Skill Gaps[/bold yellow]",
            show_header=True,
            header_style="bold yellow",
            box=box.ROUNDED,
            border_style="yellow"
        )
        
        gaps_table.add_column("Skill", style="yellow")
        gaps_table.add_column("Coverage", justify="right")
        gaps_table.add_column("Status", justify="center")
        
        for gap in matrix['skill_gaps'][:10]:  # Top 10 gaps
            coverage_pct = gap['coverage_pct']
            
            if coverage_pct < 10:
                status = "[red]Critical[/red]"
            elif coverage_pct < 20:
                status = "[yellow]Low[/yellow]"
            else:
                status = "[orange1]Medium[/orange1]"
            
            gaps_table.add_row(
                gap['skill'],
                f"{coverage_pct:.0f}%",
                status
            )
        
        self.console.print(gaps_table)
    
    def _display_knowledge_silos(self, matrix: dict):
        """Display knowledge silos"""
        if not matrix['knowledge_silos']:
            self.console.print("[green]✅ No knowledge silos detected[/green]")
            return
        
        silos_table = Table(
            title="[bold red]🔴 Knowledge Silos[/bold red]",
            show_header=True,
            header_style="bold red",
            box=box.ROUNDED,
            border_style="red"
        )
        
        silos_table.add_column("Skill", style="red")
        silos_table.add_column("Single Expert", style="bold")
        silos_table.add_column("Risk", justify="center")
        
        for silo in matrix['knowledge_silos'][:10]:
            silos_table.add_row(
                silo['skill'],
                silo['expert'],
                f"[red]{silo['risk'].upper()}[/red]"
            )
        
        self.console.print(silos_table)
    
    def _display_recommendations(self, matrix: dict):
        """Display recommendations"""
        if not matrix.get('recommendations'):
            return
        
        rec_panel = Panel(
            "\n".join([f"• {rec}" for rec in matrix['recommendations']]),
            title="[bold green]💡 Recommendations[/bold green]",
            border_style="green"
        )
        
        self.console.print(rec_panel)
    
    async def display_individual_skills(self, user_id: str):
        """
        Display individual user's skills
        """
        self.console.clear()
        
        # Header
        self.console.print(
            Panel.fit(
                f"[bold cyan]👤 Individual Skill Profile[/bold cyan]\n"
                f"[dim]User: {user_id}[/dim]",
                border_style="cyan"
            )
        )
        
        self.console.print()
        
        # Fetch skills
        async with AsyncSessionLocal() as db:
            skills = await self.skill_service.get_cached_skills(db, user_id)
        
        if not skills:
            self.console.print("[red]❌ No skill data found for this user[/red]")
            return
        
        # Display overall level
        level_color = {
            "Junior": "red",
            "Mid-Level": "yellow",
            "Mid-Level/Senior": "orange1",
            "Senior/Staff": "green"
        }.get(skills['overall_level'], "white")
        
        self.console.print(
            Panel.fit(
                f"[bold {level_color}]{skills['overall_level']}[/bold {level_color}]\n"
                f"[dim]Confidence: {skills['confidence']:.0%}[/dim]",
                title="Overall Level",
                border_style=level_color
            )
        )
        
        self.console.print()
        
        # Technical skills table
        tech_table = Table(
            title="[bold cyan]💻 Technical Skills[/bold cyan]",
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
            border_style="cyan"
        )
        
        tech_table.add_column("Skill", style="cyan", width=20)
        tech_table.add_column("Proficiency", justify="center", width=30)
        tech_table.add_column("Level", justify="center", width=12)
        tech_table.add_column("Evidence", style="dim", width=30)
        
        for skill in skills.get('technical_skills', []):
            prof_bar = self._create_skill_bar(skill['proficiency'])
            level_color = self._get_skill_color(skill['proficiency'])
            
            tech_table.add_row(
                skill['name'],
                prof_bar,
                f"[{level_color}]{skill['level']}[/{level_color}]",
                skill.get('evidence', '')[:30]
            )
        
        self.console.print(tech_table)
        
        self.console.print()
        
        # Domain expertise
        if skills.get('domain_expertise'):
            domain_table = Table(
                title="[bold magenta]🎯 Domain Expertise[/bold magenta]",
                show_header=True,
                header_style="bold magenta",
                box=box.ROUNDED,
                border_style="magenta"
            )
            
            domain_table.add_column("Area", style="magenta")
            domain_table.add_column("Proficiency", justify="center", width=30)
            domain_table.add_column("Level", justify="center")
            
            for domain in skills['domain_expertise']:
                prof_bar = self._create_skill_bar(domain['proficiency'])
                level_color = self._get_skill_color(domain['proficiency'])
                
                domain_table.add_row(
                    domain['area'],
                    prof_bar,
                    f"[{level_color}]{domain['level']}[/{level_color}]"
                )
            
            self.console.print(domain_table)


async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="View team skill matrix")
    parser.add_argument("--project", "-p", help="Project ID", default="proj_alpha")
    parser.add_argument("--user", "-u", help="User ID for individual view")
    
    args = parser.parse_args()
    
    viewer = SkillMatrixViewer()
    
    try:
        if args.user:
            await viewer.display_individual_skills(args.user)
        else:
            await viewer.display_team_skill_matrix(args.project)
    except KeyboardInterrupt:
        viewer.console.print("\n[yellow]Exited by user[/yellow]")
    except Exception as e:
        viewer.console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    asyncio.run(main())
