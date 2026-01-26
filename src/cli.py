import typer
from src.comands import app as commands_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(commands_app, name="clip", help="Komendy do historii schowka")

if __name__ == "__main__":
    app()
