# pz-mod-toolbox

Tooling for the Project Zomboid mods published from this account.

The mod repositories hold **only** the mod and its listing assets. Everything
used to build and publish them lives here: the drawing library, the listing
artwork generators, the upload pipeline and the repository template.

## Layout

```
toolbox/dibujo.py      drawing primitives and the 5x7 font (standard library only)
toolbox/publish.py     builds the package and the upload vdf, uploads, verifies
toolbox/art/katana.py listing artwork for the Katana Sharpening mod
toolbox/art/perks.py  listing artwork for the Perk Descriptions mod
template/              template for a new mod repository
CONVENCIONES.md        code, commit and release conventions
```

## Usage

Publish an existing mod:

```bash
python3 -m toolbox.publish ../pz-katana-sharpening --user YOUR_STEAM_ACCOUNT
```

That copies the mod into `workshop/Contents/mods/`, writes
`workshop/workshop_build_item.vdf`, runs steamCMD `+workshop_build_item` and
finally downloads the published item and compares it with the repository.

Regenerate the listing artwork of a mod:

```bash
python3 -m toolbox.art.katana ../pz-katana-sharpening
```

## Requirements

- Python 3.9+ (standard library only).
- [steamCMD](https://developer.valvesoftware.com/wiki/SteamCMD) for publishing,
  expected at `~/steamcmd/steamcmd.sh` or pointed at by the `STEAMCMD`
  environment variable.

## Conventions

See [`CONVENCIONES.md`](CONVENCIONES.md).

## License

GPL-3.0, see [`LICENSE`](LICENSE).
