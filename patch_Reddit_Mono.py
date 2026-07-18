#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools"]
# ///

r"""
Bake selected stylistic-set variants (e.g. ss02, ss07) into a variable
font's default glyphs, and shift the default weight.

After running, the chosen variants become the default appearance, and
toggling the same feature in an editor switches BACK to the original glyph
(GSUB direction is inverted).

https://fontdrop.info/
https://fontgauntlet.com/
https://github.com/martinus/programming-font-test-pattern

Type Yourself:
Changed variants: cv01 a, cv03 d, cv04 g, cv07 p, cv09 q, cv11 u, cv15 l
o0O s5S 9gq z2Z !|l1Iij {([|])} .,;: ``''""
a@#* vVuUwW <>;^°=-~ öÖüÜäÄßµ \/\/ -- == __
abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789 &-+@ for (int i=0; i<=j; ++i) {}
Polish diacritics: ąćęłńóśźż
"""

from patch_font import patch_font

input_path = "RedditMono[wght].ttf"
output_path = "RedditMono[wght]_patched.ttf"
wght = 450
features_to_bake = {"cv01", "cv03", "cv04", "cv07", "cv09", "cv11", "cv15"}

if __name__ == "__main__":
    patch_font(input_path, output_path, wght, features_to_bake)
