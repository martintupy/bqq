from pathlib import Path

import yaml


class Config:
    default = {
        "max_results": 1_000,
        "history_days": 30,
    }

    def __init__(self, config_path) -> None:
        self.config_path = config_path
        self._conf = None

    def write_default(self):
        Path(self.config_path).touch()
        conf = Config.default
        self._save_conf(conf)

    def _save_conf(self, conf: dict):
        self._conf = conf
        with open(self.config_path, "w") as f:
            yaml.safe_dump(conf, f)

    @property
    def conf(self) -> dict:
        if not self._conf:
            with open(self.config_path, "r") as f:
                self._conf = yaml.safe_load(f)
        return self._conf

    @property
    def project(self) -> int:
        return self.conf["project"]

    @project.setter
    def project(self, project):
        conf = {**self.conf, "project": project}
        self._save_conf(conf)

    @property
    def max_results(self) -> int:
        return self.conf["max_results"]

    @property
    def history_days(self) -> int:
        return self.conf["history_days"]
