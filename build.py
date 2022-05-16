from __future__ import annotations
from typing import TYPE_CHECKING, Final, TypeVar

from pathlib import Path
import filecmp
import importlib.machinery
import importlib.util
import shutil
import sys
import time
import traceback
import zipfile

from rangers.modbuilder import ModBuilder

sys.dont_write_bytecode = True

p_cwd = Path.cwd()
p_src = p_cwd / 'src'
p_release = p_cwd / '.release'
p_build = p_cwd / '.build'
p_update = p_cwd / '.update'
p_updates = p_cwd / '.updates'
p_update_zip = p_cwd / 'update.zip'

def pack_to_zip(folder: Path, dst: Path) -> None:
    print(f'Packing folder {folder} into {dst}...')

    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for file in folder.glob('**/*'):
            zf.write(file, file.relative_to(folder))


def load_builder(file: Path) -> ModBuilder:
    loader = importlib.machinery.SourceFileLoader(file.stem, str(file))
    spec = importlib.util.spec_from_loader(file.stem, loader)
    assert spec, (spec, file)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    builder_cls: type[ModBuilder] = module.Builder
    builder = builder_cls()
    return builder


def make_diff(
    release: Path = p_release,
    latest: Path = p_build,
    update: Path = p_update,
    updates: Path = p_updates,
    update_zip: Path = p_update_zip,
) -> None:
    update_zip_tmp = Path('update.zip.tmp')

    update.mkdir(exist_ok=True)

    for file_rel in release.rglob('*'):
        file = file_rel.relative_to(release)
        file_lat = latest / file

        if file_rel.is_dir():
            continue

        if file_lat.is_dir():
            print(f'Warning! Path {file} is file in release version, but it is a folder in latest version')
            continue

        if not file_lat.exists():
            print(f'Warning! File {file} exists in release version, but doesnt exist in latest version')
            continue

    for file_lat in latest.rglob('*'):
        file = file_lat.relative_to(latest)
        file_rel = release / file

        if file_lat.is_dir():
            continue

        if file_rel.is_dir():
            print(f'Warning! Path {file} is file in latest version, but it is a folder in release version')
            continue

        if not file_rel.exists() or not filecmp.cmp(file_rel, file_lat):
            file_upd = update / file
            if not file_upd.exists() or not filecmp.cmp(file_lat, file_upd):
                print(f'Updating file: {file}')
                file_upd.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file_lat, file_upd)

    if update_zip.exists():
        shutil.move(update_zip, update_zip_tmp)

    pack_to_zip(update, update_zip)

    if not update_zip_tmp.exists() or not filecmp.cmp(update_zip, update_zip_tmp):
        p_updates.mkdir(exist_ok=True)
        shutil.copyfile(update_zip, p_updates / f'update_{time.strftime("%Y.%m.%d %H.%M.%S")}.zip')

    if update_zip_tmp.exists():
        update_zip_tmp.unlink()



def main(
    p_src: Path = p_src,
    p_build: Path = p_build,
) -> None:
    builders: dict[str, ModBuilder] = {}

    for p_builder in list(p_src.glob('**/build.py')):
        try:
            builder = load_builder(p_builder)
            builder._src = p_builder.parent
            if builder.name in builders:
                raise NameError(builder.name, builders)
            builders[builder.name] = builder

        except Exception:
            traceback.print_exc()

    for builder_name, builder in builders.items():
        print(f'Building {builder.name}...')
        builder.build(builder._src, p_build)

    make_diff()


if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    print(f'{t2 - t1:.2} s')
