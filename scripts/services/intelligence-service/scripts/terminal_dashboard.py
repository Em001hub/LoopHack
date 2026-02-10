#!/usr/bin/env python3
"""
Intelligence Service Terminal Dashboard
Beautiful terminal UI for viewing predictions, sentiment, and insights
"""

import asyncio
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.tree import Tree
from datetime import datetime
import sys

console = Console()

API_BASE = "http://localhost:4002"


def create_header():
    """Create dashboard header"""
    text = Text()
    text.append("🧠 ", style="bold cyan")
    text.append("ProjectMind Intelligence Service", style="bold white")
    text.append(" - Real-Time Dashboard", style="dim")
    return Panel(text, style="bold blue")


def create_timeline_panel(prediction_data):
    """Create timeline prediction panel"""
    if not prediction_data:
        return Panel("No prediction data", title="📊 Timeline Prediction")
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold white")
    
    # Predicted completion
    completion = prediction_data.get('predicted_completion_date', 'N/A')
    if completion != 'N/A':
        completion = datetime.fromisoformat(completion.replace('Z', '+00:00')).strftime('%Y-%m-%d')
    
    table.add_row("📅 Predicted Completion", completion)
    table.add_row("⏱️  Weeks Remaining", f"{prediction_data.get('predicted_weeks_remaining', 0):.1f}")
    
    # Probability
    prob = prediction_data.get('probability_on_time')
    if prob is not None:
        prob_str = f"{prob:.0%}"
        if prob >= 0.8:
            prob_str = f"[green]{prob_str}[/green]"
        elif prob >= 0.6:
            prob_str = f"[yellow]{prob_str}[/yellow]"
        else:
            prob_str = f"[red]{prob_str}[/red]"
        table.add_row("✅ On-Time Probability", prob_str)
    
    # Confidence
    confidence = prediction_data.get('model_confidence', 0)
    conf_str = f"{confidence:.0%}"
    table.add_row("🎯 Model Confidence", conf_str)
    
    # Risk factors
    risks = prediction_data.get('risk_factors', [])
    if risks:
        table.add_row("")  # Spacer
        table.add_row("[bold]⚠️  Risk Factors:[/bold]", "")
        for risk in risks[:3]:
            table.add_row("  •", risk)
    
    return Panel(table, title="📊 Timeline Prediction", border_style="blue")


def create_sentiment_panel(sentiment_data):
    """Create sentiment analysis panel"""
    if not sentiment_data or sentiment_data.get('status') == 'insufficient_data':
        return Panel("Insufficient data", title="😊 Team Sentiment")
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold white")
    
    # Overall morale
    morale = sentiment_data.get('team_morale', {})
    label = morale.get('label', 'unknown')
    avg = morale.get('average_sentiment', 0)
    
    if label == 'positive':
        label_str = f"[green]{label.upper()}[/green] 😊"
    elif label == 'negative':
        label_str = f"[red]{label.upper()}[/red] 😟"
    else:
        label_str = f"[yellow]{label.upper()}[/yellow] 😐"
    
    table.add_row("Overall Morale", label_str)
    table.add_row("Average Score", f"{avg:.2f}")
    table.add_row("Trend", morale.get('trend', 'unknown'))
    
    # At-risk members
    at_risk = sentiment_data.get('at_risk_members', [])
    if at_risk:
        table.add_row("")  # Spacer
        table.add_row(f"[bold]⚠️  At Risk: {len(at_risk)}[/bold]", "")
        for member in at_risk[:2]:
            risk_level = member.get('risk_level', 'Unknown')
            table.add_row("  •", f"{risk_level} risk detected")
    
    return Panel(table, title="😊 Team Sentiment", border_style="yellow")


def create_skills_panel(skills_data):
    """Create skills matrix panel"""
    if not skills_data:
        return Panel("No skills data", title="🎯 Team Skills")
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold white")
    
    table.add_row("Team Size", str(skills_data.get('team_size', 0)))
    table.add_row("Total Skills", str(skills_data.get('coverage_stats', {}).get('total_skills', 0)))
    
    coverage = skills_data.get('coverage_stats', {}).get('coverage_score', 0)
    coverage_str = f"{coverage:.0%}"
    if coverage >= 0.8:
        coverage_str = f"[green]{coverage_str}[/green]"
    elif coverage >= 0.6:
        coverage_str = f"[yellow]{coverage_str}[/yellow]"
    else:
        coverage_str = f"[red]{coverage_str}[/red]"
    
    table.add_row("Skill Coverage", coverage_str)
    
    # Knowledge silos
    silos = len(skills_data.get('knowledge_silos', []))
    if silos > 0:
        table.add_row("")  # Spacer
        table.add_row(f"[bold]⚠️  Knowledge Silos:[/bold]", f"{silos}")
    
    return Panel(table, title="🎯 Team Skills", border_style="green")


def create_insights_panel(insights_data):
    """Create insights panel"""
    if not insights_data:
        return Panel("No insights data", title="💡 AI Insights")
    
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Insight", style="white")
    
    # Summary
    summary = insights_data.get('summary', '')
    if summary:
        table.add_row(f"[bold]{summary}[/bold]")
        table.add_row("")  # Spacer
    
    # Highlights
    highlights = insights_data.get('highlights', [])
    for highlight in highlights[:4]:
        table.add_row(highlight)
    
    # Opportunities
    opportunities = insights_data.get('opportunities', [])
    if opportunities:
        table.add_row("")  # Spacer
        table.add_row("[bold cyan]Opportunities:[/bold cyan]")
        for opp in opportunities[:2]:
            table.add_row(f"  • {opp}")
    
    return Panel(table, title="💡 AI Insights", border_style="cyan")


async def fetch_dashboard_data(project_id="proj_alpha"):
    """Fetch all data for dashboard"""
    async with httpx.AsyncClient(base_url=API_BASE, timeout=10.0) as client:
        try:
            # Fetch all data in parallel
            tasks = [
                client.post("/api/v1/predict-timeline", json={"project_id": project_id}),
                client.get(f"/api/v1/team-morale/{project_id}"),
                client.get(f"/api/v1/team-skills/{project_id}"),
                client.get(f"/api/v1/daily-insights/{project_id}"),
            ]
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            data = {}
            
            # Parse responses
            if not isinstance(responses[0], Exception) and responses[0].status_code == 200:
                data['prediction'] = responses[0].json()
            
            if not isinstance(responses[1], Exception) and responses[1].status_code == 200:
                data['sentiment'] = responses[1].json()
            
            if not isinstance(responses[2], Exception) and responses[2].status_code == 200:
                data['skills'] = responses[2].json()
            
            if not isinstance(responses[3], Exception) and responses[3].status_code == 200:
                data['insights'] = responses[3].json()
            
            return data
            
        except Exception as e:
            console.print(f"[red]Error fetching data: {e}[/red]")
            return {}


def create_dashboard_layout(data):
    """Create complete dashboard layout"""
    layout = Layout()
    
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    
    # Split main into grid
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    
    layout["left"].split_column(
        Layout(name="prediction"),
        Layout(name="sentiment")
    )
    
    layout["right"].split_column(
        Layout(name="skills"),
        Layout(name="insights")
    )
    
    # Populate panels
    layout["header"].update(create_header())
    layout["prediction"].update(create_timeline_panel(data.get('prediction')))
    layout["sentiment"].update(create_sentiment_panel(data.get('sentiment')))
    layout["skills"].update(create_skills_panel(data.get('skills')))
    layout["insights"].update(create_insights_panel(data.get('insights')))
    
    # Footer
    footer_text = Text()
    footer_text.append(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim")
    footer_text.append(" | Press Ctrl+C to exit", style="dim italic")
    layout["footer"].update(Panel(footer_text, style="dim"))
    
    return layout


async def run_dashboard(project_id="proj_alpha", refresh_seconds=10):
    """Run live dashboard"""
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]Starting Intelligence Dashboard...[/bold cyan]",
        border_style="cyan"
    ))
    
    await asyncio.sleep(1)
    
    try:
        while True:
            # Fetch data
            data = await fetch_dashboard_data(project_id)
            
            # Create layout
            layout = create_dashboard_layout(data)
            
            # Display
            console.clear()
            console.print(layout)
            
            # Wait before refresh
            await asyncio.sleep(refresh_seconds)
            
    except KeyboardInterrupt:
        console.clear()
        console.print("\n[bold cyan]Dashboard stopped.[/bold cyan]\n")


def show_prediction_details(project_id="proj_alpha"):
    """Show detailed prediction view"""
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]Fetching Timeline Prediction...[/bold cyan]",
        border_style="cyan"
    ))
    
    import httpx
    
    try:
        response = httpx.post(
            f"{API_BASE}/api/v1/predict-timeline",
            json={"project_id": project_id},
            timeout=10.0
        )
        
        if response.status_code == 200:
            data = response.json()
            
            console.clear()
            
            # Title
            console.print(Panel.fit(
                f"[bold]Timeline Prediction: {project_id}[/bold]",
                border_style="blue"
            ))
            console.print()
            
            # Main prediction
            table = Table(title="Prediction Results", show_header=True, header_style="bold cyan")
            table.add_column("Metric", style="cyan", width=30)
            table.add_column("Value", style="white", width=40)
            
            completion = datetime.fromisoformat(
                data['predicted_completion_date'].replace('Z', '+00:00')
            ).strftime('%Y-%m-%d %H:%M')
            
            table.add_row("Predicted Completion", completion)
            table.add_row("Weeks Remaining", f"{data['predicted_weeks_remaining']:.1f}")
            
            if data.get('probability_on_time'):
                prob_color = "green" if data['probability_on_time'] >= 0.7 else "yellow" if data['probability_on_time'] >= 0.5 else "red"
                table.add_row(
                    "Probability On-Time",
                    f"[{prob_color}]{data['probability_on_time']:.0%}[/{prob_color}]"
                )
            
            table.add_row("Model Confidence", f"{data['model_confidence']:.0%}")
            
            console.print(table)
            console.print()
            
            # Confidence intervals
            ci_table = Table(title="Confidence Intervals", show_header=True, header_style="bold yellow")
            ci_table.add_column("Percentile", style="yellow")
            ci_table.add_column("Date", style="white")
            
            intervals = data['confidence_intervals']
            for key in ['p10', 'p50', 'p90']:
                date_str = datetime.fromisoformat(
                    intervals[key].replace('Z', '+00:00')
                ).strftime('%Y-%m-%d')
                ci_table.add_row(key.upper(), date_str)
            
            console.print(ci_table)
            console.print()
            
            # Risk factors
            if data['risk_factors']:
                console.print("[bold red]⚠️  Risk Factors:[/bold red]")
                for risk in data['risk_factors']:
                    console.print(f"  • {risk}")
                console.print()
            
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def show_sentiment_analysis(project_id="proj_alpha"):
    """Show detailed sentiment analysis view"""
    console.clear()
    console.print(Panel.fit(
        "[bold yellow]Fetching Team Sentiment Analysis...[/bold yellow]",
        border_style="yellow"
    ))
    
    import httpx
    
    try:
        response = httpx.get(f"{API_BASE}/api/v1/team-morale/{project_id}", timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            console.clear()
            
            console.print(Panel.fit(
                f"[bold]Team Sentiment Analysis: {project_id}[/bold]",
                border_style="yellow"
            ))
            console.print()
            
            # Overall Morale
            morale = data.get('team_morale', {})
            avg_score = morale.get('average_sentiment', 0)
            label = morale.get('label', 'unknown').upper()
            icon = "😊" if label == "POSITIVE" else "😟" if label == "NEGATIVE" else "😐"
            
            console.print(f"[bold]Overall Morale:[/bold] {label} {icon}")
            console.print(f"[bold]Average Score:[/bold] {avg_score:.2f}")
            console.print(f"[bold]Movement:[/bold] {morale.get('trend', 'stable')}")
            console.print()
            
            # Stats
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Category", style="cyan")
            table.add_column("Count", style="white")
            
            table.add_row("Members Analyzed", str(data.get('members_analyzed', 0)))
            table.add_row("High Morale", f"[green]{data.get('high_morale_count', 0)}[/green]")
            table.add_row("Low Morale", f"[red]{data.get('low_morale_count', 0)}[/red]")
            
            console.print(table)
            console.print()
            
            # At Risk
            at_risk = data.get('at_risk_members', [])
            if at_risk:
                console.print("[bold red]⚠️  At-Risk Members:[/bold red]")
                for member in at_risk:
                    name = member.get('name', 'Anonymous')
                    risk = member.get('risk_level', 'Medium')
                    reason = member.get('reason', 'Burnout signals detected')
                    console.print(f"  • [bold]{name}[/bold]: {risk} Risk - [dim]{reason}[/dim]")
            else:
                console.print("[green]✅ No team members currently flagged as at-risk.[/green]")
            console.print()
            
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def show_skill_matrix(project_id="proj_alpha"):
    """Show detailed skill matrix view"""
    console.clear()
    console.print(Panel.fit(
        "[bold green]Fetching Team Skill Matrix...[/bold green]",
        border_style="green"
    ))
    
    import httpx
    
    try:
        response = httpx.get(f"{API_BASE}/api/v1/team-skills/{project_id}", timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            console.clear()
            
            console.print(Panel.fit(
                f"[bold]Team Skill Matrix: {project_id}[/bold]",
                border_style="green"
            ))
            console.print()
            
            # Key Stats
            stats = data.get('coverage_stats', {})
            coverage = stats.get('coverage_score', 0)
            
            console.print(f"[bold]Team Size:[/bold] {data.get('team_size', 0)}")
            console.print(f"[bold]Total Unique Skills:[/bold] {stats.get('total_skills', 0)}")
            console.print(f"[bold]Aggregated Coverage:[/bold] [bold green]{coverage:.0%}[/bold green]")
            console.print()
            
            # Skill Distribution
            dist_table = Table(title="Skill Distribution", show_header=True, header_style="bold cyan")
            dist_table.add_column("Skill", style="cyan")
            dist_table.add_column("Experts/Users", style="white")
            
            dist = data.get('skill_distribution', {})
            for skill, count in sorted(dist.items(), key=lambda x: x[1], reverse=True):
                dist_table.add_row(skill, "█" * count + f" ({count})")
            
            console.print(dist_table)
            console.print()
            
            # Gaps and Silos
            gaps = data.get('gaps', [])
            if gaps:
                console.print("[bold yellow]⚠️  Critical Skill Gaps:[/bold yellow]")
                for gap in gaps:
                    console.print(f"  • {gap}")
                console.print()
            
            silos = data.get('knowledge_silos', [])
            if silos:
                console.print("[bold red]⚠️  Knowledge Silos (Single Point of Failure):[/bold red]")
                for silo in silos:
                    console.print(f"  • {silo}")
                console.print()
            
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def show_daily_insights(project_id="proj_alpha"):
    """Show detailed daily insights view"""
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]Fetching Daily Insights...[/bold cyan]",
        border_style="cyan"
    ))
    
    import httpx
    
    try:
        response = httpx.get(f"{API_BASE}/api/v1/daily-insights/{project_id}", timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            console.clear()
            
            console.print(Panel.fit(
                f"[bold]Daily Insights: {project_id}[/bold]",
                border_style="cyan"
            ))
            console.print()
            
            # Summary
            console.print(f"[bold]Project Status Summary:[/bold]")
            console.print(data.get('summary', 'No summary available.'))
            console.print()
            
            # Highlights
            highlights = data.get('highlights', [])
            if highlights:
                console.print("[bold green]✅ Accomplishments:[/bold green]")
                for insight in highlights:
                    console.print(f"  • {insight}")
                console.print()
            
            # Risks
            risks = data.get('risks', [])
            if risks:
                console.print("[bold red]🚩 Identified Risks:[/bold red]")
                for risk in risks:
                    console.print(f"  • {risk}")
                console.print()
                
            # Opportunities
            opps = data.get('opportunities', [])
            if opps:
                console.print("[bold cyan]💡 Opportunities:[/bold cyan]")
                for opp in opps:
                    console.print(f"  • {opp}")
                console.print()
            
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def show_simulation_details(project_id="proj_alpha"):
    """Show detailed simulation results view"""
    console.clear()
    console.print(Panel.fit(
        "[bold magenta]Running Monte Carlo Simulation...[/bold magenta]",
        border_style="magenta"
    ))
    
    import httpx
    
    try:
        response = httpx.post(
            f"{API_BASE}/api/v1/simulate-timeline",
            json={"project_id": project_id, "n_simulations": 1000},
            timeout=15.0
        )
        
        if response.status_code == 200:
            data = response.json()
            console.clear()
            
            console.print(Panel.fit(
                f"[bold]Monte Carlo Simulation: {project_id}[/bold]",
                border_style="magenta"
            ))
            console.print()
            
            # Summary
            count = data.get('simulation_count', 1000)
            console.print(f"[bold]Simulation Detail:[/bold] {count} iterations performed.")
            
            prob = data.get('probability_on_time')
            if prob is not None:
                color = "green" if prob >= 0.8 else "yellow" if prob >= 0.6 else "red"
                console.print(f"[bold]Probability of Meeting Deadline:[/bold] [{color}]{prob:.1%}[/{color}]")
            console.print()
            
            # Percentiles
            pct_table = Table(title="Completion Percentiles", show_header=True, header_style="bold magenta")
            pct_table.add_column("Likelihood", style="magenta")
            pct_table.add_column("Weeks Required", style="white")
            pct_table.add_column("Projected Date", style="cyan")
            
            pcts = data.get('percentiles', {})
            weeks = data.get('predicted_weeks', {})
            dates = data.get('completion_dates', {})
            
            for key in ['p10', 'p25', 'p50', 'p75', 'p90']:
                label = "Optimistic (10%)" if key == 'p10' else "Median (50%)" if key == 'p50' else "Conservative (90%)" if key == 'p90' else key.upper()
                pct_table.add_row(
                    label,
                    f"{weeks.get(key, 0):.1f}",
                    dates.get(key, 'N/A').split('T')[0] if dates.get(key) else 'N/A'
                )
            
            console.print(pct_table)
            console.print()
            
            # Risk Analysis
            risk_analysis = data.get('risk_analysis', {})
            if risk_analysis:
                console.print("[bold]Risk Breakdown:[/bold]")
                for item in risk_analysis.get('risk_contribution', []):
                    console.print(f"  • {item}")
                console.print()
            
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def show_menu():
    """Show interactive menu"""
    console.clear()
    
    title = Text()
    title.append("🧠 ", style="bold cyan")
    title.append("Intelligence Service Dashboard", style="bold white")
    
    console.print(Panel.fit(title, border_style="cyan"))
    console.print()
    
    menu = Table(show_header=False, box=None)
    menu.add_column("Option", style="cyan bold", width=10)
    menu.add_column("Description", style="white")
    
    menu.add_row("1", "Live Dashboard (auto-refresh)")
    menu.add_row("2", "Timeline Prediction Details")
    menu.add_row("3", "Team Sentiment Analysis")
    menu.add_row("4", "Skill Matrix")
    menu.add_row("5", "Daily Insights")
    menu.add_row("6", "Monte Carlo Simulation")
    menu.add_row("q", "Quit")
    
    console.print(menu)
    console.print()


async def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        project_id = sys.argv[2] if len(sys.argv) > 2 else "proj_alpha"
        
        if command == "dashboard":
            await run_dashboard(project_id)
        elif command == "predict":
            show_prediction_details(project_id)
        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            console.print("Usage: python terminal_dashboard.py [dashboard|predict] [project_id]")
    else:
        # Interactive menu
        while True:
            show_menu()
            choice = console.input("[bold cyan]Select option: [/bold cyan]").strip().lower()
            
            if choice == 'q':
                console.clear()
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                break
            elif choice == '1':
                await run_dashboard()
            elif choice == '2':
                show_prediction_details()
                console.input("\n[dim]Press Enter to continue...[/dim]")
            elif choice == '3':
                show_sentiment_analysis()
                console.input("\n[dim]Press Enter to continue...[/dim]")
            elif choice == '4':
                show_skill_matrix()
                console.input("\n[dim]Press Enter to continue...[/dim]")
            elif choice == '5':
                show_daily_insights()
                console.input("\n[dim]Press Enter to continue...[/dim]")
            elif choice == '6':
                show_simulation_details()
                console.input("\n[dim]Press Enter to continue...[/dim]")
            else:
                console.print("\n[red]Invalid option[/red]\n")
                await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.clear()
        console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
