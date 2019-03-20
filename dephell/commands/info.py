# built-in
from argparse import ArgumentParser
from pathlib import Path

# app
from ..config import builders
from ..shells import Shells
from ..venvs import VEnvs
from .base import BaseCommand


class InfoCommand(BaseCommand):
    @classmethod
    def get_parser(cls):
        parser = ArgumentParser(
            prog='python3 -m dephell info',
            description='Show virtual environment information for current project.',
        )
        builders.build_config(parser)
        builders.build_venv(parser)
        builders.build_output(parser)
        builders.build_other(parser)
        parser.add_argument('key', nargs='?')
        return parser

    def __call__(self):
        venvs = VEnvs(path=self.config['venv'])
        venv = venvs.get(Path(self.config['project']))
        shells = Shells(bin_path=venv.bin_path)

        data = dict(
            exists=venv.exists(),
            venv=str(venv.path),
            project=self.config['project'],
        )

        if venv.exists():
            data.update(dict(
                activate=str(venv.bin_path / shells.current.activate),
                bin=str(venv.bin_path),
                python=str(venv.python_path),
            ))
        print(self.get_value(data=data, key=self.args.key))