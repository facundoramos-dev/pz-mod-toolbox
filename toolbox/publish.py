#!/usr/bin/env python3
"""Publishes a mod to the Steam Workshop with steamCMD.

The mod repository only holds the mod itself and its listing assets. Everything
needed to publish it (the content package, the upload vdf and the upload
command) is built here, from `workshop/ficha.json`.

Steps:
    1. copy the mod into `workshop/Contents/mods/` (the package Steam gets)
    2. build `workshop/workshop_build_item.vdf` from the ficha and local paths
    3. run steamCMD `+workshop_build_item`
    4. verify the published item against the repository

Usage:
    python3 -m toolbox.publish <mod/repo/path> [--user NAME] [--dry-run]
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

APP_ID = "108600"
STEAMCMD = os.environ.get("STEAMCMD", os.path.expanduser("~/steamcmd/steamcmd.sh"))


def load_ficha(repo):
    """Reads the listing data of a mod repository."""
    with open(repo / "workshop" / "ficha.json", encoding="utf-8") as f:
        return json.load(f)


def sync_contents(repo, ficha):
    """Copies the mod into the package folder Steam receives."""
    destino = repo / "workshop" / "Contents" / "mods"
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    for name in ficha["mods"]:
        shutil.copytree(repo / "mods" / name, destino / name)
    return destino


def build_vdf(repo, ficha, vdf_path):
    """Writes the upload vdf. The content and preview paths are absolute, so
    they are rebuilt for every clone."""
    raiz = repo.resolve()
    vdf_path.write_text(
        '"workshopitem"\n'
        "{\n"
        f'\t"appid"\t\t"{APP_ID}"\n'
        f'\t"publishedfileid"\t\t"{ficha["publishedfileid"]}"\n'
        f'\t"contentfolder"\t\t"{(raiz / "workshop" / "Contents")}"\n'
        f'\t"previewfile"\t\t"{(raiz / "workshop" / "preview.png")}"\n'
        f'\t"visibility"\t\t"{ficha.get("visibility", 0)}"\n'
        f'\t"title"\t\t"{ficha["title"]}"\n'
        f'\t"description"\t\t"{ficha["description"]}"\n'
        f'\t"changenote"\t\t"{ficha.get("changenote", "")}"\n'
        "}\n",
        encoding="utf-8")
    return vdf_path


def write_descriptions(repo, ficha):
    """Writes the per language listing texts, ready to paste in the web UI."""
    lineas = [
        f"# {ficha['title']}",
        "",
        "The upload vdf only carries one title and description, so they always land in",
        "the default slot, which the Workshop shows as **English**. The other languages",
        "are pasted by hand:",
        "",
        "> Steam Community -> the item -> *Owner controls* -> *Edit title and description*",
        "> -> pick the language -> paste -> *Save*",
        "",
        "Every upload overwrites the default slot with the contents of the vdf, so the",
        "other languages are always pasted **after** the last steamCMD upload.",
        "",
    ]
    for idioma, data in ficha.get("languages", {}).items():
        lineas += ["---", "", f"## {idioma}", "", "Title:", "", "```",
                   data["title"], "```", "", "Description:", "", "```",
                   data["description"], "```", ""]
    destino = repo / "workshop" / "descripciones.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


def upload(vdf_path, user, dry_run):
    comando = [STEAMCMD, "+login", user, "+workshop_build_item", str(vdf_path), "+quit"]
    print("+ " + " ".join(comando))
    if dry_run:
        return 0
    return subprocess.call(comando)


def verify(repo, ficha, user):
    """Downloads the published item and compares it with the repository."""
    destino = pathlib.Path("/tmp/pz-verify") / str(ficha["publishedfileid"])
    if destino.exists():
        shutil.rmtree(destino)
    subprocess.call([STEAMCMD, "+login", user,
                     "+force_install_dir", str(destino),
                     "+workshop_download_item", APP_ID, str(ficha["publishedfileid"]),
                     "+quit"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    publicado = destino / "steamapps" / "workshop" / "content" / APP_ID / str(ficha["publishedfileid"])
    ok = True
    for name in ficha["mods"]:
        origen = repo / "mods" / name
        copia = publicado / "mods" / name
        if not copia.exists():
            print(f"  {name}: NOT FOUND in the published item")
            ok = False
            continue
        igual = subprocess.call(["diff", "-r", str(origen), str(copia)]) == 0
        print(f"  {name}: {'identical' if igual else 'DIFFERENT'}")
        ok = ok and igual
    return ok


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="path to the mod repository")
    parser.add_argument("--user", default=os.environ.get("STEAM_USER", ""),
                        help="Steam account used to upload")
    parser.add_argument("--dry-run", action="store_true",
                        help="build the package and the vdf without uploading")
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    ficha = load_ficha(repo)

    print(f"Publishing {ficha['title']} ({ficha['publishedfileid']})")
    print(f"  repository: {repo}")
    destino = sync_contents(repo, ficha)
    print(f"  package:    {destino}")
    vdf = build_vdf(repo, ficha, repo / "workshop" / "workshop_build_item.vdf")
    print(f"  vdf:        {vdf}")
    write_descriptions(repo, ficha)

    codigo = upload(vdf, args.user, args.dry_run)
    if codigo != 0:
        print(f"upload failed with code {codigo}")
        return codigo

    print("verifying the published item...")
    if not verify(repo, ficha, args.user):
        print("the published item does not match the repository")
        return 1
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
