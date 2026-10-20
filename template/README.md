# MOD NAME

One paragraph: what the mod does and why it exists.

- Workshop: <https://steamcommunity.com/sharedfiles/filedetails/?id=WORKSHOP_ID>
- Mod id: `MOD_ID` (the value that goes in a server `Mods=` list)
- Requires Build 42 or newer.

## Layout

```
mods/MOD_NAME/            the mod published to the Workshop
workshop/listing.json       listing data: title, descriptions per language
workshop/preview.png      cover image, 256x256
workshop/gallery/         carousel images, 1280x720
```

The listing images and the upload itself are handled by
[pz-mod-toolbox](https://github.com/facundoramos-dev/pz-mod-toolbox).

## License

GPL-3.0, see [`LICENSE`](LICENSE).
