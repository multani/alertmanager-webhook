import click


@click.group()
def app() -> None:
    print("Run cli")


def main() -> None:
    app()
