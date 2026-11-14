#!/usr/bin/env python3
"""Finite read-only Swamp paths from already inspected literal embedded CFG; no CFG execution."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT / 'notes/analysis/T288-swamp-inspection-1.json').read_text())
cfgs = [r['text'] for r in data['embedded_records'] if r['kind'] == 5]
assert len(cfgs) == 1
cfg = cfgs[0]
models = re.findall(r'^mapmodel [0-9 -]+"([^"]+)"$', cfg, re.M)
textures = re.findall(r'^texture 0 "([^"]+)"$', cfg, re.M)
sounds = re.findall(r'^mapsound "([^"]+)" -1$', cfg, re.M)
sky = re.findall(r'^loadsky "([^"]+)"$', cfg, re.M)
assert len(models) == 55 and len(textures) == 64 and len(sounds) == 9 and len(sky) == 1
assert {int(k) for k in data['model_slots']} == set(range(55))


def info(p):
    p = p.resolve()
    assert p.is_relative_to(ROOT / 'packages')
    return dict(path=p.relative_to(ROOT).as_posix(), exists=p.is_file(),
                bytes=p.stat().st_size if p.is_file() else None)


rows = []
for slot, name in enumerate(models):
    directory = ROOT / 'packages/models/mapmodels' / name
    # Native tries MD2 first; these Swamp directories use literal MD3 configs.
    assert not (directory / 'tris.md2').exists() and not (directory.parent / 'tris.md2').exists()
    config = directory / 'md3.cfg'
    assert config.is_file()
    text = config.read_text()
    # Read literal Cube CFG words, preserving apostrophes inside double quotes;
    # this is not a shell/Cube evaluator.
    commands = [[a or b for a, b in re.findall(r'"([^"]*)"|(\S+)', line.split('//', 1)[0])]
                for line in text.splitlines()]
    commands = [c for c in commands if c and not c[0].startswith('//')]
    geometry = [info(directory / c[1]) for c in commands if c[0] == 'md3load']
    skins = [info(directory / c[2]) for c in commands if c[0] == 'md3skin']
    if not geometry:  # md3::load default branch after metadata-only CFG.
        geometry = [info(next(p for p in (directory / 'tris.md3', directory.parent / 'tris.md3') if p.is_file()))]
        skins = [info(next(p for p in (directory / 'skin.jpg', directory / 'skin.png',
                                      directory.parent / 'skin.jpg', directory.parent / 'skin.png') if p.is_file()))]
    assert geometry and skins
    rows.append(dict(slot=slot, name=name, geometry=geometry, skins=skins,
                     config=info(config), commands=commands,
                     config_text=text,
                     direct_files=[p.name for p in sorted(directory.iterdir()) if p.is_file()] if directory.is_dir() else []))
texture_rows = [dict(slot=i, used=i in data['texture_slots'], **info(ROOT / 'packages/textures' / name))
                for i, name in enumerate(textures)]
sky_rows = [info(ROOT / 'packages/textures/skymaps' / (sky[0] + '_' + face + '.jpg'))
            for face in ('lf', 'rt', 'ft', 'bk', 'dn', 'up')]
sound_rows = [dict(slot=i, **info(ROOT / 'packages/audio' / name)) for i, name in enumerate(sounds)]
all_paths = [ROOT / r['path'] for r in texture_rows + sky_rows + sound_rows]
for r in rows:
    all_paths += [ROOT / x['path'] for x in r['geometry'] + r['skins'] + [r['config']]]
notice_paths = set()
for path in all_paths:
    for parent in path.parents:
        if parent == ROOT or not parent.is_relative_to(ROOT / 'packages'):
            break
        for p in parent.iterdir():
            if p.is_file() and any(term in p.name.lower() for term in ('license', 'licence', 'copyright', 'readme')):
                notice_paths.add(p)
notices = [dict(path=p.relative_to(ROOT).as_posix(), text=p.read_text(errors='replace')) for p in sorted(notice_paths)]
print(json.dumps(dict(models=rows, textures=texture_rows, sky=sky_rows, sounds=sound_rows,
                      notices=notices,
                      optional_map_cfg={name:(ROOT / name).exists() for name in
                                        ('packages/maps/ac_swamp.cfg', 'packages/maps/official/ac_swamp.cfg')}), indent=2))
