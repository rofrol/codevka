#!/usr/bin/env bash
set -e
# https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-located-from-within/246128#246128
DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
echo ${DIR}

family="$1"
variant="$2"
extension="$3"
file_orig="${family}-${variant}.${extension}"
file="${family}NerdFont-${variant}.${extension}"
ln -sf ${DIR}/private-build-plans-${family}.toml ${DIR}/vendor/Iosevka/private-build-plans.toml
cd ${DIR}/vendor/Iosevka
npm run build -- ttf-unhinted::${family}
cp "${DIR}/vendor/Iosevka/dist/${family}/TTF-Unhinted/${file_orig}" ${DIR}/
cd ${DIR}/vendor/FontPatcher
#
## Test with `ghostty +list-fonts` or `kitty +list-fonts --psnames`
## --makegroups needed to have Postscript name https://github.com/ryanoasis/nerd-fonts/issues/579#issuecomment-1441612101
## Postscript name may be needed for kitty when disabling ligatures with -liga
## https://github.com/kovidgoyal/kitty/issues/2738#issuecomment-854384969
fontforge -script font-patcher --complete "${DIR}/vendor/Iosevka/dist/${family}/TTF-Unhinted/${file_orig}"
cp "$file" ${DIR}/

uv run ${DIR}/fix-mono-font.py ${DIR}/"$file"
[ -f "${HOME}/Library/Fonts/$file" ] && rm "${HOME}/Library/Fonts/$file"
open -a Font\ Book "$DIR/$file"
rm "$file"
