import pytest

from src.manga_archiver.cli.commands import parse_args
from src.manga_archiver.cli.presets import get_preset_names

ARGPARSE_USAGE_ERROR = 2


class TestParseArgs:
    def test_defaults_to_application_command_options(self) -> None:
        args = parse_args([])

        assert args.command is None
        assert args.preset == "default"
        assert args.archive is False
        assert args.benchmark is False
        assert args.backlog is False
        assert args.headless is False

    @pytest.mark.parametrize("preset", get_preset_names(), ids=get_preset_names())
    def test_parses_preset_option(self, preset: str) -> None:
        args = parse_args(["--preset", preset])

        assert args.preset == preset

    def test_rejects_invalid_preset(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            parse_args(["--preset", "balanced"])

        assert exc_info.value.code == ARGPARSE_USAGE_ERROR

    @pytest.mark.parametrize("auth_action", ["login", "logout"], ids=["login", "logout"])
    def test_parses_auth_subcommands(self, auth_action: str) -> None:
        args = parse_args(["auth", "google-drive", auth_action])

        assert args.command == "auth"
        assert args.auth_provider == "google-drive"
        assert args.auth_action == auth_action

    @pytest.mark.parametrize(
        "migrate_system",
        ["database", "google-drive"],
        ids=["database", "google-drive"],
    )
    def test_parses_migrate_subcommands(self, migrate_system: str) -> None:
        args = parse_args(["migrate", migrate_system])

        assert args.command == "migrate"
        assert args.migrate_system == migrate_system

    def test_parses_list_presets_subcommand(self) -> None:
        args = parse_args(["list", "presets"])

        assert args.command == "list"
        assert args.list_target == "presets"

    def test_parses_config_discord_subcommand(self) -> None:
        args = parse_args(["config", "webhooks", "discord"])

        assert args.command == "config"
        assert args.config_category == "webhooks"
        assert args.config_target == "discord"

    @pytest.mark.parametrize(
        ("argv", "expected_command", "expected_subcommands"),
        [
            (
                ["--archive", "auth", "google-drive", "login"],
                "auth",
                {"auth_provider": "google-drive", "auth_action": "login"},
            ),
            (
                ["--archive", "migrate", "database"],
                "migrate",
                {"migrate_system": "database"},
            ),
            (
                ["--archive", "config", "webhooks", "discord"],
                "config",
                {"config_category": "webhooks", "config_target": "discord"},
            ),
        ],
        ids=["archive-auth-login", "archive-migrate-database", "archive-config-discord"],
    )
    def test_parses_global_flags_with_subcommands(
        self,
        argv: list[str],
        expected_command: str,
        expected_subcommands: dict[str, str],
    ) -> None:
        args = parse_args(argv)

        assert args.archive is True
        assert args.command == expected_command
        for subcommand_name, subcommand in expected_subcommands.items():
            assert getattr(args, subcommand_name) == subcommand

    @pytest.mark.parametrize(
        "argv",
        [["auth"], ["auth", "google-drive"], ["migrate"], ["config"], ["config", "webhooks"]],
        ids=[
            "missing-auth-provider",
            "missing-auth-action",
            "missing-migrate-subcommand",
            "missing-config-category",
            "missing-config-target",
        ],
    )
    def test_requires_nested_subcommands(self, argv: list[str]) -> None:
        with pytest.raises(SystemExit) as exc_info:
            parse_args(argv)

        assert exc_info.value.code == ARGPARSE_USAGE_ERROR

    def test_rejects_unknown_command(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            parse_args(["unknowncmd"])

        assert exc_info.value.code == ARGPARSE_USAGE_ERROR

    def test_rejects_removed_auto_exit_flag(self) -> None:
        with pytest.raises(SystemExit) as exc_info:
            parse_args(["--auto-exit"])

        assert exc_info.value.code == ARGPARSE_USAGE_ERROR

    def test_parses_headless_with_archive_and_backlog(self) -> None:
        args = parse_args(["--archive", "--backlog", "--headless"])

        assert args.archive is True
        assert args.backlog is True
        assert args.headless is True

    @pytest.mark.parametrize(
        "argv",
        [
            ["--headless"],
            ["--archive", "--headless"],
            ["--backlog", "--headless"],
        ],
        ids=["missing-both", "missing-backlog", "missing-archive"],
    )
    def test_rejects_headless_without_archive_and_backlog(self, argv: list[str]) -> None:
        with pytest.raises(SystemExit) as exc_info:
            parse_args(argv)

        assert exc_info.value.code == ARGPARSE_USAGE_ERROR
