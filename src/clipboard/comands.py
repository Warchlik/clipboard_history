import hashlib
import time
from typing import Optional
import pyperclip
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import delete
import typer

from clipboard.database import get_db, init_database
from clipboard.models import Clips


app = typer.Typer(no_args_is_help=True)


def get_paste() -> str:
    try:
        return pyperclip.paste() or ""
    except Exception:
        return ""


def set_copy(value: str) -> None:
    pyperclip.copy(value)


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()


def delete_similar_record(db: Session, content_hash: str) -> None:
    similar_clip: Optional[Clips] = db.scalars(
        select(Clips).where(Clips.content_hash == content_hash)
    ).one_or_none()

    if similar_clip:
        db.delete(similar_clip)


@app.command()
def watch(
    poll: float = typer.Option(0.5, "--poll", help="Co ile sekund sprawdzać schowek"),
):
    init_database()
    db = next(get_db())
    last_hash: str | None = None
    try:
        while True:
            copy_value = get_paste()

            if not copy_value:
                continue

            hashed_value: str = sha256(copy_value)

            if hashed_value == last_hash:
                continue

            last_hash = hashed_value

            delete_similar_record(db=db, content_hash=hashed_value)

            clip: Optional[Clips] = Clips(content=copy_value, content_hash=hashed_value)
            db.add(clip)
            db.commit()
            time.sleep(poll)
    except KeyboardInterrupt:
        typer.secho("\n Bye")


# TODO: fix listing value errors
@app.command()
def list(number: int = typer.Argument(20, help="How many clips you will got to show")):
    init_database()

    db: Session = next(get_db())

    clips = db.scalars(select(Clips).order_by(Clips.id.desc()).limit(number)).all()

    if not clips:
        typer.secho("No clips you have in past")

    for clip in clips:
        typer.secho(message=f"{clip.id} {clip.content}")


@app.command()
def prune():
    init_database()

    db: Session = next(get_db())

    try:
        result = db.execute(delete(Clips))

        db.commit()
        typer.secho(f"\nYour clips history has been deleted: {result}")

    except Exception:
        typer.secho("\nSomting goes wrong, try again")


@app.command()
def search(
    value: str = typer.Argument("", help="Tap what you wona to find in your history"),
):
    init_database()

    db: Session = next(get_db())

    if len(value) == 0:
        return

    result_clips = db.scalars(
        select(Clips).where(Clips.content.like(f"%{value}%"))
    ).all()

    if not result_clips:
        typer.secho("\nCan not find by sentense")

    for clip in result_clips:
        typer.secho(f"\n{clip.id} {clip.content} {clip.content_hash}")


# TODO: add interval method witch prune history by self
