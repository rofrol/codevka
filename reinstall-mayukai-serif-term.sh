#!/usr/bin/env bash
# https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-located-from-within-the-script/246128#246128
DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
echo ${DIR}
ln -sf ${DIR}/private-build-plans-mayukai-serif-term.toml ${DIR}/vendor/Iosevka/private-build-plans.toml &&
  cd ${DIR}/vendor/Iosevka &&
  npm run build -- ttf-unhinted::iosevka-mayukai-serif &&
  cp ${DIR}/vendor/Iosevka/dist/iosevka-mayukai-serif/TTF-Unhinted/iosevka-mayukai-serif-ExtendedBook.ttf ${DIR}/ &&
  cp ${DIR}/vendor/Iosevka/dist/iosevka-mayukai-serif/TTF-Unhinted/iosevka-mayukai-serif-ExtendedSemiLight.ttf ${DIR}/ &&
  cd ${DIR}/vendor/FontPatcher &&
  ## seems like this makegroups does not work for `kitty +list-fonts --psnames`
  ## --makegroups needed to have Postscript name https://github.com/ryanoasis/nerd-fonts/issues/579#issuecomment-1441612101
  ## Postscript name may be needed for kitty when disabling ligatures wiht -liga
  ## https://github.com/kovidgoyal/kitty/issues/2738#issuecomment-854384969
  fontforge -script font-patcher --makegroups --complete ${DIR}/vendor/Iosevka/dist/iosevka-mayukai-serif/TTF-Unhinted/iosevka-mayukai-serif-ExtendedBook.ttf &&
  cp IosevkaMayukaiSerifNerdFont-Extended.ttf ${DIR}/ &&
  open -a Font\ Book ${DIR}/IosevkaMayukaiSerifNerdFont-Extended.ttf &&
  fontforge -script font-patcher --makegroups --complete ${DIR}/vendor/Iosevka/dist/iosevka-mayukai-serif/TTF-Unhinted/iosevka-mayukai-serif-ExtendedSemiLight.ttf &&
  cp IosevkaMayukaiSerifNerdFont-ExtendedSemiLight.ttf ${DIR}/ &&
  open -a Font\ Book ${DIR}/IosevkaMayukaiSerifNerdFont-ExtendedSemiLight.ttf
