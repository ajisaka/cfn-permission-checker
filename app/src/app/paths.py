from pathlib import Path

from app_paths import AppPaths

_paths = AppPaths.get_paths("cfn-permission-checker", "synm", "0.1.0")
UserDataDirectory: Path = _paths.user_data_path
