# Conventions

## Code

- **English only.** Identifiers, comments, docstrings and commit messages are
  in English. The only exception is content that is *published* in another
  language: the Spanish and English listing texts in `workshop/listing.json`.
- **Comments explain why, not what.** The code should read as the intention,
  not as a transcript of itself.
- **Standard library only.** The listing images are generated with `zlib` and
  `struct` so that they can be rebuilt anywhere without installing anything.
- **No machine specific paths in the repositories.** The upload vdf needs
  absolute paths, so it is generated at publish time by `toolbox/publish.py`
  and git ignored.

## Commits

Every commit follows the structured format:

```text
[Type] Title

Description of what changed and why, with the touched files referenced as
relative paths in backticks, for example `mods/KatanaSharpening/42/mod.info`.
```

Allowed types: `Feat`, `Refactor`, `Fix`, `Test`, `Doc`, `Chore`.

## Mod repositories

A mod repository holds:

```
mods/<ModName>/          the mod published to the Workshop
workshop/listing.json      listing data: title, descriptions per language
workshop/preview.png     cover image, 256x256
workshop/gallery/        carousel images, 1280x720
README.md
LICENSE
```

Build artifacts (`workshop/Contents/`, `workshop/workshop_build_item.vdf`,
`workshop/descriptions.md`) are generated and git ignored.

## Releases

1. Change the mod and bump `version` and `modversion` in its `mod.info`.
2. Update the listing data in `workshop/listing.json` and the `changenote`.
3. Commit with a `[Feat]`, `[Fix]` or `[Chore]` message.
4. Publish: `python3 -m toolbox.publish <repo> --user <account>`.
5. Tag the release: `git tag v<version>`.

## Workshop listing

- The upload vdf carries **one** title and description, so they always land in
  the default slot, which the Workshop shows as *English*. The other languages
  are pasted by hand from the text `toolbox/publish.py` writes to
  `workshop/descriptions.md`: *Owner controls* → *Edit title and
  description* → pick the language → *Save*.
- Every upload overwrites the default slot, so the other languages are always
  pasted **after** the last upload.
- The cover image and the carousel images are also uploaded from the web:
  *Owner controls* → *Add/Edit images and videos*.
- Tags are set by the game client (`ISteamUGC::SetItemTags` runs at upload
  time, and the vdf has no field for them): *Submit Mod to Workshop* → *Existing
  Item* → tick the tags → publish.

## What the upload vdf can and cannot do

The vdf carries the content, the cover, the title, the description, the change
note and the visibility. It has **no** field for the rest:

| Missing | Why | Where to do it |
|---|---|---|
| Other languages | one title and description only | web UI, per language |
| Carousel images | one `previewfile` only | web UI |
| Tags | set by `ISteamUGC::SetItemTags` at upload time | game client |
| Per item dependencies, links, comments | not part of the vdf | web UI |

Tag ids for Project Zomboid, for tools that ask for them by id:

| Tag | id | | Tag | id |
|---|---|---|---|---|
| Build 42 | 448331 | | Weapons | 274770 |
| Balance | 266335 | | Items | 203294 |
| Interface | 203292 | | QoL | 228474 |
| Multiplayer | 274768 | | Misc | 274767 |
| Framework | 205122 | | Building | 44746 |
| Language/Translation | 274766 | | WIP | 448778 |

The full list is embedded in the browse page JSON:
<https://steamcommunity.com/workshop/browse/?appid=108600&section=readytouseitems>

## Gotchas

- The VDF parser does **not** interpret `\n` escapes: line breaks in a title or
  description have to be written literally in the file, otherwise the Workshop
  page shows the text `\n` instead of a line break.
- No double quotes inside a vdf value: use `[i]...[/i]`, `[b]...[/b]` or avoid
  them.
