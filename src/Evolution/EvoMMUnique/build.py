from __future__ import annotations
from pathlib import Path

import rangers.modbuilder


class Builder(rangers.modbuilder.ModBuilder):
    name = 'EvoMMUnique'
    script_name = 'Mod_EvoMMUnique'

    path = Path(f'Mods/Evolution/{name}')

    def build(self, src: Path, dst: Path) -> None:
        self.compile_script_and_patch_dats(
            dst / self.path,
            self.path,
            src / f'{self.script_name}.rson',
            self.script_name,
            src / 'Lang_rus.txt',
            None,  # src / 'Lang_eng.txt',
            None,  # src / 'script_text_eng.txt',
            src / 'CacheData.txt',
            src / 'Main.txt',
        )
        self.copy_folder(src / 'DATA', dst / self.path / 'DATA')
        self.copy_file(src / 'ModuleInfo.txt', dst / self.path / 'ModuleInfo.txt')


if __name__ == '__main__':
    Builder()._build()
