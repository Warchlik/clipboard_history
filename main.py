from typing import Optional
import typer
import pyperclip
import time
import hashlib

app = typer.Typer(no_args_is_help=True)


def sha256(value: str) -> Optional[str]:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()


# TODO: dodać komendy oraz dodać integrację z bazą dancyh


def show_clipboarded() -> None:
    last_hash = ""

    while True:
        try:
            value = pyperclip.paste() or ""

            curent_hash = sha256(value)
            if curent_hash == last_hash:
                continue

            last_hash = curent_hash

            print(value + "\n")
        except Exception:
            continue

        time.sleep(0.5)


if __name__ == "__main__":
    show_clipboarded()
