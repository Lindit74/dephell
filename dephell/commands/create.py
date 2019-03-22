
# built-in
from argparse import ArgumentParser
from pathlib import Path

# external
from dephell_pythons import Python, Pythons

# app
from ..config import builders
from ..converters import CONVERTERS
from ..venvs import VEnvs
from .base import BaseCommand


class CreateCommand(BaseCommand):
    @classmethod
    def get_parser(cls):
        parser = ArgumentParser(
            prog='python3 -m dephell create',
            description='Create virtual environment for current project.',
        )
        builders.build_config(parser)
        builders.build_from(parser)
        builders.build_venv(parser)
        builders.build_output(parser)
        builders.build_other(parser)
        return parser

    def _get_python(self) -> Python:
        pythons = Pythons()

        # defined in config
        python = self.config.get('python')
        if python:
            return pythons.get_best(python)

        # defined in dependency file
        loader = CONVERTERS[self.config['from']['format']]
        root = loader.load(path=self.config['from']['path'])
        if root.python:
            return pythons.get_by_spec(root.python)

        return pythons.current

    def __call__(self) -> bool:
        venvs = VEnvs(path=self.config['venv'])
        venv = venvs.get(Path(self.config['project']), env=self.config.env)
        if venv.exists():
            self.logger.warning('venv already exists', extra=dict(path=venv.path))
            return False

        self.logger.info('creating venv for project...', extra=dict(path=venv.path))
        python = self._get_python()
        self.logger.debug('choosen python', extra=dict(version=python.version))
        venv.create(python_path=python.path)
        return True