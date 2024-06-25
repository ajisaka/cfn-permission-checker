import json
from datetime import datetime
from typing import Any, Sequence

import click
from dateutil import tz
from scalpl import Cut

from app.collector import collect_records
from app.filter import Filter
from app.paths import UserDataDirectory


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    # ctx.obj = App()
    pass


@main.command("filter")
@click.option("--from", "from_", type=str, default="1h")
@click.option("--error-only", "-e", help="Only error records", type=bool, default=False, is_flag=True)
@click.option("--error-code", "-c", "error_codes", help="Filter by error code", type=str, default=None, multiple=True)
@click.option("--show-message", "-m", help="Show error message", type=bool, default=False, is_flag=True)
@click.option("--show-property", "-p", help="Show property valuessage", type=str, multiple=True)
@click.option(
    "--unauthorized-operation",
    "-u",
    help="Same as `--error Client.UnauthorizedOperation`",
    type=bool,
    is_flag=True,
    default=False,
)
@click.option("--show-actions", "-a", help="Show actions only", type=bool, is_flag=True, default=False)
def cmd_collect_actions(
    from_: str,
    error_codes: Sequence[str],
    unauthorized_operation: bool,
    show_actions: bool,
    error_only: bool,
    show_message: bool,
    show_property: Sequence[str],
) -> None:
    ecs = list(error_codes)

    if unauthorized_operation:
        ecs.append("Client.UnauthorizedOperation")

    filter = Filter(from_=from_, error_codes=ecs, error_only=error_only)

    if show_actions:
        actions = set()
        for record in collect_records(filter):
            if filter.match(record):
                actions.add(_build_action_string(record))
        for action in sorted(actions):
            print(action)
        return

    for record in collect_records(filter):
        print(f"""{_to_local_time(record["eventTime"])} {_build_action_string(record)}""")
        if "errorCode" in record:
            print(f"""    {record["errorCode"]}""")
            if show_message:
                if "errorMessage" in record:
                    print(f"""      {record["errorMessage"]}""")
                if record.get("responseElements") != None:
                    if "message" in record["responseElements"]:
                        print(f"""        {record["responseElements"]["message"]}""")
        for prop in show_property:
            value = Cut(record)[prop]
            if value is not None:
                print(f"""    {prop}: {json.dumps(value)}""")


@main.command("paths")
def cmd_paths() -> None:
    print(f"""UserDataDirectory: {UserDataDirectory}""")


def _build_action_string(record: Any) -> str:
    source = record["eventSource"]
    name = record["eventName"]
    return f"""{source.split(".")[0]}:{name}"""


def _to_local_time(dt: str) -> str:
    _dt = datetime.fromisoformat(dt)
    return _dt.astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    main()
