import hashlib
from shutil import copy
import time
from typing import Optional
import pyperclip
from sqlalchemy import select
from sqlalchemy.orm import Session
import typer

from src.database import get_db, init_database
from src.models import Clips


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
    similar_clip: Optional[Clips] = db.execute(
        select(Clips).where(Clips.content_hash == content_hash)
    ).scalar_one_or_none()

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
def list(number: int = typer.Argument(20, help="Ile wpisów pokazać")):
    init_database()

    db: Session = next(get_db())

    clips = db.execute(select(Clips).order_by(Clips.id.desc()).limit(number)).all()

    if not clips:
        typer.secho("No clips you have in past")

    for clip in clips:
        typer.secho(message=f"{clip.id} {clip.content}")


# TODO: add methods for serach copied value in history
# TODO: add method for prune all data from clips history
# TODO: add interval method witch prune history by self
