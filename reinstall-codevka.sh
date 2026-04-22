#!/usr/bin/env bash
# https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-located-from-within/246128#246128
DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
echo ${DIR}

# uv handles dependencies (fonttools) automatically via inline script metadata

ln -sf ${DIR}/private-build-plans-Codevka.toml ${DIR}/vendor/Iosevka/private-build-plans.toml &&
  cd ${DIR}/vendor/Iosevka &&
  # npm run build -- ttf-unhinted::Codevka &&
  # cp ${DIR}/vendor/Iosevka/dist/Codevka/TTF-Unhinted/Codevka-ExtendedSemiLight.ttf ${DIR}/ &&
  # cp ${DIR}/vendor/Iosevka/dist/Codevka/TTF-Unhinted/Codevka-Extended.ttf ${DIR}/ &&
  cd ${DIR}/vendor/FontPatcher &&
  ## seems like this makegroups does not work for `kitty +list-fonts --psnames`
  ## --makegroups needed to have Postscript name https://github.com/ryanoasis/nerd-fonts/issues/579#issuecomment-1441612101
  ## Postscript name may be needed for kitty when disabling ligatures with -liga
  ## https://github.com/kovidgoyal/kitty/issues/2738#issuecomment-854384969
  # fontforge -script font-patcher --makegroups --complete ${DIR}/vendor/Iosevka/dist/Codevka/TTF-Unhinted/Codevka-ExtendedSemiLight.ttf &&
  # fontforge -script font-patcher --makegroups --complete ${DIR}/vendor/Iosevka/dist/Codevka/TTF-Unhinted/Codevka-Extended.ttf &&
  cp CodevkaNerdFont-ExtendedSemiLight.ttf ${DIR}/ &&
  cp CodevkaNerdFont-Extended.ttf ${DIR}/ &&

  # Fix isFixedPitch + PostScript names after NerdFont patching.
  # FontForge resets post.isFixedPitch=0, causing macOS to not recognize the font
  # as monospace in Font Book, and kitty +list-fonts --psnames to not list it.
  uv run ${DIR}/fix-nerd-font.py \
    ${DIR}/CodevkaNerdFont-Extended.ttf \
    ${DIR}/CodevkaNerdFont-ExtendedSemiLight.ttf &&

  rm /Users/romanfrolow/Library/Fonts/CodevkaNerdFont-Extended.ttf &&
  rm /Users/romanfrolow/Library/Fonts/CodevkaNerdFont-ExtendedSemiLight.ttf &&
  open -a Font\ Book ${DIR}/CodevkaNerdFont-ExtendedSemiLight.ttf &&
  open -a Font\ Book ${DIR}/CodevkaNerdFont-Extended.ttf
