"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """fwscan."""


if __name__ == "__main__":
    main(prog_name="fwscan")  # pragma: no cover
