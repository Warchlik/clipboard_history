import typer
from clipboard.comands import app as commands_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(commands_app, help="Komendy do historii schowka")

if __name__ == "__main__":
    app()
