#!/usr/bin/env python3
"""
Terminal Dashboard for Intelligence Service
Beautiful rich terminal UI showing predictions, sentiment, and insights
"""

import asyncio
import sys
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box
import httpx

# Configuration
API_BASE_URL = "http://localhost:8002/api/v1"

console = Console()


class IntelligenceDashboard:
    """Real-time dashboard for intelligence service"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.console = Console()
    
    async def fetch_predictions(self) -> dict:
        """Fetch timeline predictions"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{API_BASE_URL}/predict-timeline",
                    json={"project_id": self.project_id},
                    timeout=30.0
                )
                return response.json() if response.status_code == 200 else {}
            except Exception as e:
                return {"error": str(e)}
    
    async def fetch_team_sentiment(self) -> dict:
        """Fetch team sentiment data"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{API_BASE_URL}/team-sentiment/{self.project_id}",
                    timeout=30.0
                )
                return response.json() if response.status_code == 200 else {}
            except Exception as e:
                return {"error": str(e)}
    
    async def fetch_project_insights(self) -> dict:
        """Fetch project insights"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{API_BASE_URL}/project-insights/{self.project_id}",
                    timeout=30.0
                )
                return response.json() if response.status_code == 200 else {}
            except Exception as e:
                return {"error": str(e)}
    
    def create_header(self) -> Panel:
        """Create dashboard header"""
        title = Text("🧠 Intelligence Service Dashboard", style="bold cyan")
        subtitle = Text(f"Project: {self.project_id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                       style="dim")
        
        content = Text()
        content.append(title)
        content.append("\n")
        content.append(subtitle)
        
        return Panel(
            content,
            box=box.DOUBLE,
            style="cyan"
        )
    
    def create_prediction_panel(self, prediction_data: dict) -> Panel:
        """Create timeline prediction panel"""
        if "error" in prediction_data:
            return Panel(
                f"[red]Error: {prediction_data['error']}[/red]",
                title="📊 Timeline Prediction",
                border_style="red"
            )
        
        if not prediction_data:
            return Panel(
                "[yellow]Loading predictions...[/yellow]",
                title="📊 Timeline Prediction"
            )
        
        # Parse data
        predicted_date = prediction_data.get('predicted_completion_date', 'N/A')
        weeks = prediction_data.get('predicted_weeks_remaining', 0)
        
        # Format dates
        try:
            pred_dt = datetime.fromisoformat(predicted_date)
            predicted_str = pred_dt.strftime('%B %d, %Y')
            days_remaining = (pred_dt - datetime.now()).days
        except:
            predicted_str = predicted_date
            days_remaining = int(weeks * 7) if weeks else 0
        
        # Create content
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Label", style="bold")
        table.add_column("Value")
        
        table.add_row(
            "Predicted Completion:",
            f"[bold green]{predicted_str}[/bold green] ({days_remaining} days)"
        )
        table.add_row(
            "Weeks Remaining:",
            f"[cyan]{weeks:.1f} weeks[/cyan]"
        )
        
        # Risk factors
        risks = prediction_data.get('risk_factors', [])
        if risks:
            table.add_row("", "")  # Spacer
            table.add_row(
                "[bold red]⚠️  Risk Factors:[/bold red]",
                ""
            )
            for risk in risks[:3]:  # Show top 3
                table.add_row(
                    "",
                    f"[yellow]• {risk}[/yellow]"
                )
        
        return Panel(
            table,
            title="📊 Timeline Prediction",
            border_style="green"
        )
    
    def create_sentiment_panel(self, sentiment_data: dict) -> Panel:
        """Create team sentiment panel"""
        if "error" in sentiment_data:
            return Panel(
                f"[red]Error: {sentiment_data['error']}[/red]",
                title="😊 Team Sentiment",
                border_style="red"
            )
        
        if not sentiment_data:
            return Panel(
                "[yellow]Loading sentiment data...[/yellow]",
                title="😊 Team Sentiment"
            )
        
        # Create content
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Label", style="bold")
        table.add_column("Value")
        
        table.add_row(
            "Overall Sentiment:",
            f"[green]Positive[/green]"
        )
        table.add_row(
            "Team Size:",
            f"{sentiment_data.get('members_analyzed', 'N/A')} members"
        )
        
        return Panel(
            table,
            title="😊 Team Sentiment",
            border_style="green"
        )
    
    def create_insights_panel(self, insights_data: dict) -> Panel:
        """Create project insights panel"""
        if "error" in insights_data:
            return Panel(
                f"[red]Error: {insights_data['error']}[/red]",
                title="💡 Insights",
                border_style="red"
            )
        
        if not insights_data:
            return Panel(
                "[yellow]Loading insights...[/yellow]",
                title="💡 Insights"
            )
        
        # Create content
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Insight", style="cyan")
        
        insights = insights_data.get('insights', [])
        if insights:
            for insight in insights[:5]:
                table.add_row(f"• {insight}")
        else:
            table.add_row("[dim]No insights available[/dim]")
        
        return Panel(
            table,
            title="💡 Insights",
            border_style="cyan"
        )
    
    async def run(self):
        """Run the dashboard"""
        with Live(
            self.create_header(),
            console=self.console,
            refresh_per_second=1,
            screen=False
        ) as live:
            while True:
                try:
                    # Fetch all data in parallel
                    prediction_data, sentiment_data, insights_data = await asyncio.gather(
                        self.fetch_predictions(),
                        self.fetch_team_sentiment(),
                        self.fetch_project_insights()
                    )
                    
                    # Create layout
                    layout = Layout()
                    layout.split_column(
                        Layout(self.create_header(), size=5),
                        Layout(name="main")
                    )
                    
                    # Split main into columns
                    layout["main"].split_row(
                        Layout(self.create_prediction_panel(prediction_data)),
                        Layout(name="right_column")
                    )
                    
                    # Right column
                    layout["right_column"].split_column(
                        Layout(self.create_sentiment_panel(sentiment_data)),
                        Layout(self.create_insights_panel(insights_data))
                    )
                    
                    live.update(layout)
                    
                    # Refresh every 30 seconds
                    await asyncio.sleep(30)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
                    await asyncio.sleep(5)


async def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        console.print("[red]Usage: terminal_dashboard.py <project_id>[/red]")
        console.print("Example: terminal_dashboard.py proj_alpha")
        sys.exit(1)
    
    project_id = sys.argv[1]
    
    console.print(f"[cyan]Starting Intelligence Dashboard for {project_id}...[/cyan]")
    console.print("[dim]Press Ctrl+C to exit[/dim]\n")
    
    dashboard = IntelligenceDashboard(project_id)
    await dashboard.run()


if __name__ == "__main__":
    asyncio.run(main())
