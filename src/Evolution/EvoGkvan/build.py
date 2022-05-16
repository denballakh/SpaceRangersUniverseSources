from __future__ import annotations
from pathlib import Path

import rangers.modbuilder


class Builder(rangers.modbuilder.ModBuilder):
    name = 'EvoGkvan'

    path = Path(f'Mods/Evolution/{name}')

    def build(self, src: Path, dst: Path) -> None:
        self.txt_to_dat(
            src / 'Lang_rus.txt',
            dst / self.path / 'CFG' / 'Rus' / 'Lang.dat',
            fmt='HDMain',
        )
        # self.txt_to_dat(
        #     src / 'Lang_eng.txt',
        #     dst / self.path / 'CFG' / 'Eng' / 'Lang.dat',
        #     fmt='HDMain',
        # )
        self.txt_to_dat(
            src / 'Main.txt',
            dst / self.path / 'CFG' / 'Main.dat',
            fmt='HDMain',
        )
        self.txt_to_dat(
            src / 'Lang_rus.txt',
            dst / self.path / 'CFG' / 'CacheData.dat',
            fmt='HDCache',
        )
        self.copy_file(src / 'ModuleInfo.txt', dst / self.path / 'ModuleInfo.txt')


if __name__ == '__main__':
    Builder()._build()
