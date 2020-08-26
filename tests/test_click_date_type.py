import click
from click_date_type import Date


def test_date_option_default(runner):
    @click.command()
    @click.option("--start_date", type=Date())
    def cli(start_date):
        click.echo(start_date.strftime("%Y-%m-%d"))

    result = runner.invoke(cli, ["--start_date=2015-09-29"])
    assert not result.exception
    assert result.output == "2015-09-29\n"

    result = runner.invoke(cli, ["--start_date=2015-09"])
    assert result.exit_code == 2
    assert (
        "Invalid value for '--start_date':"
        " invalid date format: 2015-09."
        " (choose from %Y-%m-%d)"
    ) in result.output

    result = runner.invoke(cli, ["--help"])
    assert "--start_date [%Y-%m-%d]" in result.output


def test_date_option_custom(runner):
    @click.command()
    @click.option("--start_date", type=Date(formats=["%A %B %d, %Y"]))
    def cli(start_date):
        click.echo(start_date.strftime("%Y-%m-%d"))

    result = runner.invoke(cli, ["--start_date=Wednesday June 05, 2010"])
    assert not result.exception
    assert result.output == "2010-06-05\n"
