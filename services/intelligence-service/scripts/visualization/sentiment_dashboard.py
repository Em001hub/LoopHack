"""
Sentiment Dashboard
Real-time ASCII visualization of team morale and burnout risk
"""
import time
import random
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich import box
from datetime import datetime, timedelta

class SentimentDashboard:
    def __init__(self):
        self.team_members = ["Alice", "Bob", "Charlie", "David", "Eve"]
        self.history = {m: [0.0] * 20 for m in self.team_members}
        
    def generate_sparkline(self, data):
        """Generate ASCII sparkline from data list"""
        bars = u" ▂▃▅▆▇"
        min_val, max_val = -1.0, 1.0
        range_val = max_val - min_val
        
        sparkline = ""
        for x in data:
            # Normalize to 0-5 index
            normalized = (x - min_val) / range_val
            idx = int(normalized * (len(bars) - 1))
            idx = max(0, min(idx, len(bars) - 1))
            
            # Color coding
            color = "green" if x > 0.3 else "red" if x < -0.3 else "yellow"
            sparkline += f"[{color}]{bars[idx]}[/{color}]"
            
        return sparkline

    def update_data(self):
        """Simulate new sentiment data"""
        for member in self.team_members:
            # Random walk
            prev = self.history[member][-1]
            change = random.uniform(-0.3, 0.3)
            new_val = max(-1.0, min(1.0, prev + change))
            self.history[member].pop(0)
            self.history[member].append(new_val)

    def make_layout(self) -> Layout:
        layout = Layout(name="root")
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["main"].split_row(
            Layout(name="members"),
            Layout(name="alerts")
        )
        return layout

    def generate_member_table(self):
        table = Table(box=box.SIMPLE, expand=True)
        table.add_column("Member")
        table.add_column("Current")
        table.add_column("Trend (20 days)")
        table.add_column("Risk")

        for member in self.team_members:
            current = self.history[member][-1]
            trend = self.generate_sparkline(self.history[member])
            
            # Risk calc
            avg_last_5 = sum(self.history[member][-5:]) / 5
            if avg_last_5 < -0.5:
                risk = "[bold red]HIGH[/]"
            elif avg_last_5 < -0.2:
                risk = "[yellow]MED[/]"
            else:
                risk = "[green]LOW[/]"

            score_color = "green" if current > 0 else "red"
            table.add_row(
                member,
                f"[{score_color}]{current:.2f}[/]",
                trend,
                risk
            )
        return Panel(table, title="Team Sentiment & Burnout Risk")

    def generate_alerts(self):
        # Find active alerts
        alerts = []
        for member in self.team_members:
            if self.history[member][-1] < -0.7:
                alerts.append(f"[bold red]![/] {member} reported extreme frustration")
            if sum(self.history[member][-3:]) / 3 < -0.5:
                alerts.append(f"[bold yellow]![/] {member} showing sustained stress")
                
        if not alerts:
            content = "[green]No active alerts. Team morale is stable.[/]"
        else:
            content = "\n".join(alerts)
            
        return Panel(Align.center(content, vertical="middle"), title="Active Alerts")

    def run(self):
        layout = self.make_layout()
        layout["header"].update(Panel(Align.center("[bold magenta]ProjectMind AI Sentiment Tracker[/]"), style="on black"))
        
        with Live(layout, refresh_per_second=2, screen=True):
            # Run for a short demo duration to prevent infinite loop
            start_time = time.time()
            while time.time() - start_time < 5:  # Run for 5 seconds
                self.update_data()
                layout["members"].update(self.generate_member_table())
                layout["alerts"].update(self.generate_alerts())
                layout["footer"].update(Align.center(f"Last updated: {datetime.now().strftime('%H:%M:%S')}"))
                time.sleep(1)

if __name__ == "__main__":
    try:
        dashboard = SentimentDashboard()
        dashboard.run()
    except KeyboardInterrupt:
        print("Dashboard stopped.")
