#!/usr/bin/env python3
"""
Monte Carlo Simulation Visualizer
Displays simulation results with distribution charts in terminal
"""

import sys
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from datetime import datetime

console = Console()

API_BASE_URL = "http://localhost:8002/api/v1"


def create_ascii_histogram(distribution: dict, width: int = 60) -> str:
    """Create ASCII histogram from distribution data"""
    bins = distribution.get('bins', [])
    counts = distribution.get('counts', [])
    
    if not bins or not counts:
        return "No distribution data available"
    
    max_count = max(counts) if counts else 1
    lines = []
    
    # Title
    lines.append("Distribution of Completion Times:")
    lines.append("")
    
    # Create bars
    for i, (bin_start, count) in enumerate(zip(bins, counts)):
        # Normalize to width
        bar_length = int((count / max_count) * width)
        bar = "█" * bar_length
        
        # Format bin label
        weeks = f"{bin_start:.1f}"
        
        # Create line
        line = f"{weeks:>6} weeks │{bar} {count}"
        lines.append(line)
    
    return "\n".join(lines)


def visualize_simulation(project_id: str, scenario_params: dict = None):
    """Visualize Monte Carlo simulation results"""
    console.print(f"[cyan]Running Monte Carlo simulation for {project_id}...[/cyan]\n")
    
    # Call API
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{API_BASE_URL}/run-simulation",
                json={
                    "project_id": project_id,
                    "n_simulations": 1000,
                    "scenario_params": scenario_params or {}
                }
            )
            
            if response.status_code != 200:
                console.print(f"[red]Error: {response.text}[/red]")
                return
            
            data = response.json()
    except Exception as e:
        console.print(f"[red]Error calling API: {e}[/red]")
        return
    
    # Display results
    console.print(Panel(
        f"[bold]Monte Carlo Simulation Results[/bold]\n"
        f"Project: {project_id}\n"
        f"Simulations: {data.get('simulation_count', 0):,}",
        box=box.DOUBLE,
        style="cyan"
    ))
    
    # Summary statistics
    weeks = data.get('predicted_weeks', {})
    
    summary_table = Table(title="📊 Summary Statistics", box=box.ROUNDED)
    summary_table.add_column("Metric", style="bold")
    summary_table.add_column("Value", style="cyan")
    
    summary_table.add_row("Mean", f"{weeks.get('mean', 0):.2f} weeks")
    summary_table.add_row("Median", f"{weeks.get('median', 0):.2f} weeks")
    summary_table.add_row("Std Dev", f"{weeks.get('std', 0):.2f} weeks")
    summary_table.add_row("Min", f"{weeks.get('min', 0):.2f} weeks")
    summary_table.add_row("Max", f"{weeks.get('max', 0):.2f} weeks")
    
    console.print(summary_table)
    console.print()
    
    # Percentiles table
    percentiles = data.get('percentiles', {})
    
    percentile_table = Table(title="📈 Confidence Intervals", box=box.ROUNDED)
    percentile_table.add_column("Percentile", style="bold")
    percentile_table.add_column("Weeks", style="cyan")
    
    for p_label, p_key in [("10th", "p10"), ("25th", "p25"), ("50th (Median)", "p50"), 
                           ("75th", "p75"), ("90th", "p90")]:
        weeks_val = percentiles.get(p_key, 0)
        percentile_table.add_row(p_label, f"{weeks_val:.2f}")
    
    console.print(percentile_table)
    console.print()
    
    # Distribution histogram
    distribution = data.get('distribution', {})
    if distribution:
        histogram = create_ascii_histogram(distribution, width=50)
        
        console.print(Panel(
            histogram,
            title="📊 Distribution Histogram",
            border_style="cyan"
        ))
        console.print()


def compare_scenarios(project_id: str):
    """Compare multiple what-if scenarios"""
    console.print(f"[cyan]Comparing scenarios for {project_id}...[/cyan]\n")
    
    scenarios = [
        {
            "name": "Add 2 Developers",
            "add_developers": 2
        },
        {
            "name": "Cut 20% Features",
            "reduce_scope_pct": 20
        }
    ]
    
    # Call API
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                f"{API_BASE_URL}/compare-scenarios",
                json={
                    "project_id": project_id,
                    "scenarios": scenarios,
                    "n_simulations": 500
                }
            )
            
            if response.status_code != 200:
                console.print(f"[red]Error: {response.text}[/red]")
                return
            
            data = response.json()
    except Exception as e:
        console.print(f"[red]Error calling API: {e}[/red]")
        return
    
    # Display comparison
    console.print(Panel(
        "[bold]Scenario Comparison[/bold]",
        box=box.DOUBLE,
        style="cyan"
    ))
    
    # Comparison table
    comparison_table = Table(title="📊 Scenario Results", box=box.ROUNDED)
    comparison_table.add_column("Scenario", style="bold cyan")
    comparison_table.add_column("Median Weeks", style="green")
    comparison_table.add_column("P90 Weeks", style="yellow")
    
    for row in data.get('comparison_table', []):
        comparison_table.add_row(
            row.get('scenario', 'Unknown'),
            f"{row.get('median_weeks', 0):.1f}",
            f"{row.get('p90_weeks', 0):.1f}"
        )
    
    console.print(comparison_table)
    console.print()
    
    # Recommendation
    recommendation = data.get('recommendation', 'No recommendation available')
    console.print(Panel(
        f"[bold green]Recommendation:[/bold green]\n{recommendation}",
        style="green"
    ))


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        console.print("[red]Usage:[/red]")
        console.print("  simulation_visualizer.py <project_id>              # Run single simulation")
        console.print("  simulation_visualizer.py <project_id> compare      # Compare scenarios")
        sys.exit(1)
    
    project_id = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "single"
    
    if mode == "compare":
        compare_scenarios(project_id)
    else:
        visualize_simulation(project_id)


if __name__ == "__main__":
    main()
