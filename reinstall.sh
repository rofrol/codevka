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
##--name "${family} NF ${variant}"
## makegroups is choosing how font is named. used bc error: name too long
## https://github.com/ryanoasis/nerd-fonts/wiki/ScriptOptions
## https://github.com/ryanoasis/nerd-fonts/discussions/1754
# --dry
fontforge -script font-patcher --complete --debug 2 --makegroups 4 "${DIR}/vendor/Iosevka/dist/${family}/TTF-Unhinted/${file_orig}"

mv "$file" ${DIR}/

uv run ${DIR}/fpfix.py ${DIR}/"$file"
[ -f "${HOME}/Library/Fonts/$file" ] && rm "${HOME}/Library/Fonts/$file"
open -a Font\ Book "$DIR/$file"
