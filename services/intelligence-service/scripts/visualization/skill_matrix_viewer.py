"""
Skill Matrix Terminal Viewer
Displays team skill heatmaps using Rich
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
import sys
import random

# Mock data generator (replace with API call in production)
def get_mock_skill_matrix():
    skills = ["Python", "React", "AWS", "SQL", "Docker", "Kubernetes", "TypeScript"]
    team = ["Alice", "Bob", "Charlie", "David", "Eve"]
    
    matrix = {}
    for skill in skills:
        matrix[skill] = {}
        for member in team:
            # 0.0 to 1.0 proficiency
            matrix[skill][member] = random.random()
            
    return skills, team, matrix

def get_color_for_score(score: float) -> str:
    """Return color hex based on proficiency score"""
    if score >= 0.8: return "green"      # Expert
    if score >= 0.6: return "bright_green" # Advanced
    if score >= 0.4: return "yellow"     # Intermediate
    if score >= 0.2: return "red"        # Beginner
    return "bright_black"                # Novice/None

def display_skill_matrix():
    console = Console()
    skills, team, matrix = get_mock_skill_matrix()
    
    # Create Table
    table = Table(
        title="Engineering Team Skill Matrix",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold magenta"
    )
    
    # Add Columns
    table.add_column("Skill / Member", style="bold white", width=20)
    for member in team:
        table.add_column(member, justify="center")
        
    # Add Rows
    for skill in skills:
        row_data = [skill]
        for member in team:
            score = matrix[skill][member]
            color = get_color_for_score(score)
            
            # Determine symbol/text
            if score >= 0.8: level = "Expert"
            elif score >= 0.6: level = "Adv"
            elif score >= 0.4: level = "Mid"
            elif score >= 0.2: level = "Beg"
            else: level = "-"
            
            cell = Text(level, style=color)
            if score >= 0.8:
                cell.append(" ★", style="gold1")
                
            row_data.append(cell)
            
        table.add_row(*row_data)
        
    # Legend
    legend = Text.assemble(
        ("Expert (0.8+)", "green"), "  ",
        ("Advanced (0.6+)", "bright_green"), "  ",
        ("Intermediate (0.4+)", "yellow"), "  ",
        ("Beginner (0.2+)", "red"), "  ",
        ("Novice (<0.2)", "bright_black")
    )
    
    console.print()
    console.print(table)
    console.print(Panel(legend, title="Proficiency Levels", expand=False))

if __name__ == "__main__":
    display_skill_matrix()
