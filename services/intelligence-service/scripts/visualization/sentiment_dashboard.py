"""
Sentiment Dashboard
Real-time team morale and sentiment visualization
"""

import asyncio
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box
from rich.progress import BarColumn, Progress, TextColumn
from datetime import datetime
from loguru import logger

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.services.sentiment_service import SentimentService
from src.config.database import AsyncSessionLocal


class SentimentDashboard:
    """
    Live updating sentiment dashboard
    """
    
    def __init__(self):
        self.console = Console()
        self.sentiment_service = SentimentService()
    
    def _get_sentiment_emoji(self, score: float) -> str:
        """Get emoji based on sentiment score"""
        if score >= 0.3:
            return "😊"
        elif score >= 0:
            return "😐"
        elif score >= -0.3:
            return "😟"
        else:
            return "😢"
    
    def _get_sentiment_color(self, score: float) -> str:
        """Get color based on sentiment"""
        if score >= 0.3:
            return "green"
        elif score >= 0:
            return "yellow"
        elif score >= -0.3:
            return "orange1"
        else:
            return "red"
    
    def _get_risk_color(self, level: str) -> str:
        """Get color based on risk level"""
        colors = {
            "Low": "green",
            "Medium": "yellow",
            "High": "red"
        }
        return colors.get(level, "white")
    
    def _create_sentiment_gauge(self, score: float, width: int = 30) -> str:
        """Create visual gauge for sentiment"""
        # Normalize score from [-1, 1] to [0, 1]
        normalized = (score + 1) / 2
        
        filled = int(normalized * width)
        empty = width - filled
        
        color = self._get_sentiment_color(score)
        
        gauge = "█" * filled + "░" * empty
        return f"[{color}]{gauge}[/{color}]"
    
    async def create_dashboard_layout(self, project_id: str) -> Layout:
        """
        Create dashboard layout
        """
        # Fetch team morale
        async with AsyncSessionLocal() as db:
            morale = await self.sentiment_service.analyze_team_morale(db, project_id, days=14)
        
        # Create layout
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Header
        header_text = Text()
        header_text.append("🎭 Team Sentiment Dashboard", style="bold cyan")
        header_text.append(f"\nProject: {project_id} | ", style="dim")
        header_text.append(f"Updated: {datetime.now().strftime('%H:%M:%S')}", style="dim")
        
        layout["header"].update(Panel(header_text, border_style="cyan"))
        
        # Body - split into sections
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["body"]["left"].split_column(
            Layout(name="team_overview"),
            Layout(name="at_risk")
        )
        
        layout["body"]["right"].split_column(
            Layout(name="members"),
            Layout(name="trends")
        )
        
        # Team Overview
        layout["body"]["left"]["team_overview"].update(
            self._create_team_overview_panel(morale)
        )
        
        # At Risk Members
        layout["body"]["left"]["at_risk"].update(
            self._create_at_risk_panel(morale)
        )
        
        # Individual Members
        layout["body"]["right"]["members"].update(
            self._create_members_panel(morale)
        )
        
        # Trends (placeholder)
        layout["body"]["right"]["trends"].update(
            self._create_trends_panel(morale)
        )
        
        # Footer
        footer_text = Text()
        footer_text.append("Press Ctrl+C to exit | ", style="dim")
        footer_text.append("Updates every 30 seconds", style="dim italic")
        
        layout["footer"].update(Panel(footer_text, border_style="blue"))
        
        return layout
    
    def _create_team_overview_panel(self, morale: dict) -> Panel:
        """Create team overview panel"""
        team_morale = morale['team_morale']
        
        score = team_morale['average_sentiment']
        emoji = self._get_sentiment_emoji(score)
        label = team_morale['label']
        color = self._get_sentiment_color(score)
        
        # Create gauge
        gauge = self._create_sentiment_gauge(score)
        
        overview_table = Table(show_header=False, box=None, padding=0)
        overview_table.add_column("Metric", style="cyan")
        overview_table.add_column("Value", style="bold")
        
        overview_table.add_row(
            "Overall Mood",
            f"{emoji} [{color}]{label}[/{color}]"
        )
        overview_table.add_row(
            "Sentiment Score",
            f"{gauge} [{color}]{score:+.2f}[/{color}]"
        )
        overview_table.add_row(
            "Trend",
            f"[{'green' if team_morale['trend'] == 'improving' else 'red'}]{team_morale['trend'].upper()}[/]"
        )
        overview_table.add_row("", "")
        overview_table.add_row(
            "😊 High Morale",
            f"[green]{morale['high_morale_count']}[/green]"
        )
        overview_table.add_row(
            "😐 Medium Morale",
            f"[yellow]{morale['members_analyzed'] - morale['high_morale_count'] - morale['low_morale_count']}[/yellow]"
        )
        overview_table.add_row(
            "😟 Low Morale",
            f"[red]{morale['low_morale_count']}[/red]"
        )
        
        return Panel(
            overview_table,
            title="[bold]Team Overview[/bold]",
            border_style=color,
            padding=(1, 2)
        )
    
    def _create_at_risk_panel(self, morale: dict) -> Panel:
        """Create at-risk members panel"""
        at_risk = morale['at_risk_members']
        
        if not at_risk:
            return Panel(
                "[green]✅ No team members at risk[/green]",
                title="[bold]⚠️  At-Risk Members[/bold]",
                border_style="green"
            )
        
        risk_table = Table(
            show_header=True,
            header_style="bold red",
            box=box.SIMPLE,
            padding=0
        )
        
        risk_table.add_column("Member", style="red", width=15)
        risk_table.add_column("Risk", justify="center", width=8)
        risk_table.add_column("Score", justify="right", width=5)
        
        for member in at_risk[:5]:  # Top 5
            risk_color = self._get_risk_color(member['risk_level'])
            
            risk_table.add_row(
                member['user_id'][:15],
                f"[{risk_color}]{member['risk_level']}[/{risk_color}]",
                f"[{risk_color}]{member['risk_score']}[/{risk_color}]"
            )
        
        return Panel(
            risk_table,
            title=f"[bold red]⚠️  At-Risk Members ({len(at_risk)})[/bold red]",
            border_style="red",
            padding=(1, 1)
        )
    
    def _create_members_panel(self, morale: dict) -> Panel:
        """Create individual members panel"""
        member_details = morale.get('member_details', {})
        
        members_table = Table(
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE,
            padding=0
        )
        
        members_table.add_column("Member", style="cyan", width=15)
        members_table.add_column("Mood", justify="center", width=5)
        members_table.add_column("Sentiment", justify="right", width=25)
        
        # Sort by sentiment
        sorted_members = sorted(
            member_details.items(),
            key=lambda x: x[1].get('current_sentiment', {}).get('recent_avg', 0),
            reverse=True
        )
        
        for user_id, details in sorted_members[:8]:  # Top 8
            if details.get('status') == 'insufficient_data':
                continue
            
            score = details['current_sentiment']['recent_avg']
            emoji = self._get_sentiment_emoji(score)
            color = self._get_sentiment_color(score)
            
            mini_gauge = self._create_sentiment_gauge(score, width=15)
            
            members_table.add_row(
                user_id[:15],
                emoji,
                f"{mini_gauge} [{color}]{score:+.2f}[/{color}]"
            )
        
        return Panel(
            members_table,
            title="[bold]👥 Team Members[/bold]",
            border_style="cyan",
            padding=(1, 1)
        )
    
    def _create_trends_panel(self, morale: dict) -> Panel:
        """Create trends panel"""
        # Simple trend visualization
        team_morale = morale['team_morale']
        
        trend_text = Text()
        
        if team_morale['trend'] == 'improving':
            trend_text.append("📈 ", style="green")
            trend_text.append("Morale Improving", style="bold green")
            trend_text.append("\n\nTeam sentiment is on an upward trajectory. ", style="green")
            trend_text.append("Keep up the good work!", style="green")
        elif team_morale['trend'] == 'declining':
            trend_text.append("📉 ", style="red")
            trend_text.append("Morale Declining", style="bold red")
            trend_text.append("\n\nTeam sentiment is decreasing. ", style="red")
            trend_text.append("Consider team check-in.", style="red")
        else:
            trend_text.append("➡️  ", style="yellow")
            trend_text.append("Morale Stable", style="bold yellow")
            trend_text.append("\n\nTeam sentiment is steady.", style="yellow")
        
        return Panel(
            trend_text,
            title="[bold]📊 Trends[/bold]",
            border_style="blue",
            padding=(1, 2)
        )
    
    async def run_live_dashboard(self, project_id: str, refresh_interval: int = 30):
        """
        Run live updating dashboard
        """
        self.console.clear()
        
        with Live(
            await self.create_dashboard_layout(project_id),
            refresh_per_second=1,
            console=self.console
        ) as live:
            try:
                while True:
                    await asyncio.sleep(refresh_interval)
                    live.update(await self.create_dashboard_layout(project_id))
            except KeyboardInterrupt:
                pass


async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Live sentiment dashboard")
    parser.add_argument("--project", "-p", help="Project ID", default="proj_alpha")
    parser.add_argument("--refresh", "-r", type=int, default=30, help="Refresh interval (seconds)")
    
    args = parser.parse_args()
    
    dashboard = SentimentDashboard()
    
    try:
        await dashboard.run_live_dashboard(args.project, args.refresh)
    except KeyboardInterrupt:
        dashboard.console.print("\n[yellow]Dashboard stopped[/yellow]")
    except Exception as e:
        dashboard.console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    asyncio.run(main())
