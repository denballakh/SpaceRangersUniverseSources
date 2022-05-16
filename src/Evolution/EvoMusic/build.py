from __future__ import annotations
from pathlib import Path

import rangers.modbuilder


class Builder(rangers.modbuilder.ModBuilder):
    name = 'EvoMusic'

    path = Path(f'Mods/Evolution/{name}')

    def build(self, src: Path, dst: Path) -> None:
        self.txt_to_dat(
            src / 'Main.txt',
            dst / self.path / 'CFG' / 'Main.dat',
            fmt='HDMain',
        )
        self.copy_folder(src / 'DATA', dst / self.path / 'DATA')
        self.copy_file(src / 'ModuleInfo.txt', dst / self.path / 'ModuleInfo.txt')


if __name__ == '__main__':
    Builder()._build()
