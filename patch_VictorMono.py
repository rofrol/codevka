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
Changed variants: ss02 0, ss07 69
o0O s5S 9gq z2Z !|l1Iij {([|])} .,;: ``''""
a@#* vVuUwW <>;^°=-~ öÖüÜäÄßµ \/\/ -- == __
abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789 &-+@ for (int i=0; i<=j; ++i) {}
Polish diacritics: ąćęłńóśźż
"""

from patch_font import patch_font

input_path = "VictorMono-VariableFont_wght.ttf"
output_path = "VictorMono-VariableFont_wght_patched.ttf"
wght = 650
features_to_bake = {"ss02", "ss07"}

if __name__ == "__main__":
    patch_font(input_path, output_path, wght, features_to_bake)
