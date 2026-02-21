import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from database import Database
from models import Creator, Partnership

app = typer.Typer(help="CLI tool to discover and manage micro-influencer partnerships")
console = Console()
db = Database()

@app.command()
def search(
    platform: str = typer.Option(None, help="Platform (youtube/instagram/tiktok)"),
    niche: str = typer.Option(None, help="Niche/category"),
    min_followers: int = typer.Option(None, help="Minimum followers"),
    max_followers: int = typer.Option(None, help="Maximum followers")
):
    """Search for creators by filters"""
    creators = db.search_creators(platform, niche, min_followers, max_followers)
    
    if not creators:
        console.print("[yellow]No creators found matching criteria[/yellow]")
        return
    
    table = Table(title="Search Results")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Platform", style="blue")
    table.add_column("Niche", style="magenta")
    table.add_column("Followers", style="yellow")
    table.add_column("Engagement", style="red")
    
    for creator in creators:
        table.add_row(
            str(creator['id']),
            creator['name'],
            creator['platform'],
            creator['niche'],
            f"{creator['followers']:,}",
            f"{creator['engagement_rate']:.2f}%"
        )
    
    console.print(table)

@app.command()
def add(
    name: str = typer.Argument(..., help="Creator name"),
    platform: str = typer.Argument(..., help="Platform"),
    niche: str = typer.Argument(..., help="Niche/category"),
    followers: int = typer.Argument(..., help="Follower count"),
    engagement_rate: float = typer.Argument(..., help="Engagement rate %"),
    contact: str = typer.Option(None, help="Contact email/handle")
):
    """Add a new creator to database"""
    creator = Creator(name, platform, niche, followers, engagement_rate, contact)
    creator_id = db.add_creator(creator)
    console.print(f"[green]✓[/green] Creator added with ID: {creator_id}")

@app.command()
def analyze(creator_id: int = typer.Argument(..., help="Creator ID")):
    """Analyze creator performance metrics"""
    creator = db.get_creator(creator_id)
    
    if not creator:
        console.print("[red]Creator not found[/red]")
        return
    
    # Calculate metrics
    engagement_score = "High" if creator['engagement_rate'] > 5 else "Medium" if creator['engagement_rate'] > 2 else "Low"
    follower_tier = "Micro" if creator['followers'] < 100000 else "Mid" if creator['followers'] < 500000 else "Macro"
    
    panel_content = f"""
[bold]Name:[/bold] {creator['name']}
[bold]Platform:[/bold] {creator['platform']}
[bold]Niche:[/bold] {creator['niche']}
[bold]Followers:[/bold] {creator['followers']:,}
[bold]Engagement Rate:[/bold] {creator['engagement_rate']:.2f}%
[bold]Engagement Score:[/bold] {engagement_score}
[bold]Tier:[/bold] {follower_tier}
[bold]Contact:[/bold] {creator['contact'] or 'N/A'}
    """
    
    console.print(Panel(panel_content, title=f"Creator Analysis - ID {creator_id}", border_style="blue"))

@app.command()
def partner(
    creator_id: int = typer.Argument(..., help="Creator ID"),
    status: str = typer.Option("contacted", help="Status (contacted/negotiating/active/completed)"),
    budget: float = typer.Option(0.0, help="Budget allocated"),
    notes: str = typer.Option("", help="Partnership notes")
):
    """Create or update partnership record"""
    partnership = Partnership(creator_id, status, budget, notes)
    partnership_id = db.add_partnership(partnership)
    console.print(f"[green]✓[/green] Partnership record created with ID: {partnership_id}")

@app.command()
def partnerships(creator_id: int = typer.Option(None, help="Filter by creator ID")):
    """List all partnerships"""
    records = db.get_partnerships(creator_id)
    
    if not records:
        console.print("[yellow]No partnership records found[/yellow]")
        return
    
    table = Table(title="Partnership Records")
    table.add_column("ID", style="cyan")
    table.add_column("Creator", style="green")
    table.add_column("Status", style="blue")
    table.add_column("Budget", style="yellow")
    table.add_column("ROI", style="red")
    table.add_column("Notes", style="white")
    
    for record in records:
        roi = f"{record['roi']:.1f}%" if record['roi'] else "N/A"
        table.add_row(
            str(record['id']),
            record['creator_name'],
            record['status'],
            f"${record['budget']:.2f}",
            roi,
            record['notes'][:30] + "..." if len(record['notes']) > 30 else record['notes']
        )
    
    console.print(table)

@app.command()
def update_roi(
    partnership_id: int = typer.Argument(..., help="Partnership ID"),
    revenue: float = typer.Argument(..., help="Revenue generated")
):
    """Update partnership ROI"""
    db.update_partnership_roi(partnership_id, revenue)
    console.print(f"[green]✓[/green] ROI updated for partnership {partnership_id}")

@app.command()
def list_creators():
    """List all creators in database"""
    creators = db.get_all_creators()
    
    if not creators:
        console.print("[yellow]No creators in database. Use 'add' command to add creators.[/yellow]")
        return
    
    table = Table(title="All Creators")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Platform", style="blue")
    table.add_column("Niche", style="magenta")
    table.add_column("Followers", style="yellow")
    
    for creator in creators:
        table.add_row(
            str(creator['id']),
            creator['name'],
            creator['platform'],
            creator['niche'],
            f"{creator['followers']:,}"
        )
    
    console.print(table)

if __name__ == "__main__":
    app()
