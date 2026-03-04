# Codevka

My customization of [Iosevka font](https://github.com/be5invis/Iosevka) based on ss09 Source Code Pro variant.

- No ligatures, no italics, no bold.
- Nerd font patched. Needed for vscode. Otherwise you can fallback to <https://github.com/ryanoasis/nerd-fonts/releases/latest/download/NerdFontsSymbolsOnly.tar.xz>.
- All icons with `--complete`.
- weights: Regular for terminal, SemiLight for vscode
- widths: Extended to match wide characters of Source Code Pro
![](screenshot.png)

## Naming

If your font name in private-build-plans.toml contains string `SourceCode`, it will be replaced with `SauceCode`.

## spacing: term vs fixed

> The variant Iosevka Term is designed to better support terminals and the variant Iosevka Fixed omits the ligatures. <https://en.wikipedia.org/wiki/Iosevka>

Terminal (“Term”)：A narrower variant focusing terminal uses. Arrows and geometric symbols will be narrow to follow typical terminal usages.

Fixed: Exact monospace font without ligatures and wide glyphs. Since some environments cannot interpret Iosevka or Iosevka Term as monospace, and have difficulties with ligatures included, you can use Iosevka Fixed as an alternative.

<https://github.com/be5invis/Iosevka/blob/main/doc/PACKAGE-LIST.md>

## Other fonts

- <https://github.com/Iosevka-Mayukai/Iosevka-Mayukai>
- <https://github.com/saumyajyoti/MiosevkaNerdFont>
- <https://github.com/protesilaos/aporetic>

## Run

I have generated `private-build-plans.toml` at <https://typeof.net/Iosevka/customizer>

- Overview of stylistic sets <https://github.com/be5invis/Iosevka/blob/main/doc/stylistic-sets.md>
  - <https://news.ycombinator.com/item?id=36785409>
  - <https://github.com/aaronmbos/monocode/blob/main/src/private-build-plans.toml>
  - <https://github.com/shytikov/pragmasevka/blob/main/private-build-plans.toml>
  - <https://git.sr.ht/~ashton314/iosevka-output/tree/main/item/private-build-plans.toml>

Requirements:

```shell
brew install ttfautohint fontforge python-setuptools
mkdir -p vendor && cd vendor
git clone --depth 1 https://github.com/be5invis/Iosevka.git
cd Iosevka
npm install
cd ..
# Currently downloaded FontPatcher from master, because there was fix but no new release:
# curl -OJNL https://github.com/ryanoasis/nerd-fonts/raw/refs/heads/master/FontPatcher.zip
curl -OJNL https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FontPatcher.zip
unzip FontPatcher.zip -d FontPatcher
rm FontPatcher.zip
cd ..
```

`./reinstall-codevka.sh`

or

`watchexec -e toml,sh -c -r ./reinstall-codevka.sh`

## Ghostty

`font-family = Codevka Nerd Font`

## Links

- <https://lambdaland.org/posts/2022-08-01_a_new_font/>
- <https://protesilaos.com/emacs/iosevka-comfy-pictures>
- <https://kau.sh/blog/build-iosevka-font-mac-os/>
- <https://github.com/NNBnh/dotfiles/wiki/font>
