from rich.console import Console
from rich.theme import Theme

# Rich Theme
fwtheme = Theme({"success": "green", "error": "bold red"})

# Rich console handle
console = Console(theme=fwtheme)