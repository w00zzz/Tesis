from rich.console import Console
from rich.table import Table

from rich import box

def printdf(df, titulo):
    console = Console()
    table = Table(
        title=f"[bold blue]{titulo}[/bold blue]", 
        header_style="bold white on blue", 
        box=box.DOUBLE_EDGE,
        show_lines=True
    )
    
    columns = list(df.columns)
    for column in columns:
        table.add_column(column, justify="center")
        
    for _, row in df.iterrows():
        table.add_row(*[str(row[col]) for col in columns])
        
    console.print(table)