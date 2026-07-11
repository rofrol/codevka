#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools"]
# ///

"""
https://fontdrop.info/
https://github.com/martinus/programming-font-test-pattern

Type Yourself:
Changed variants: cv01 a, cv03 d, cv04 g, cv07 p, cv09 q, cv11 u, cv15 l
o0O s5S 9gq z2Z !|l1Iij {([|])} .,;: ``''""
a@#* vVuUwW <>;^°=-~ öÖüÜäÄßµ \/\/ -- == __
abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789 &-+@ for (int i=0; i<=j; ++i) {}
Polish diacritics: ąćęłńóśźż
"""

import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

wght = 450


def patch_reddit_mono():
    global wght
    input_path = "RedditMono[wght].ttf"
    output_path = "RedditMono[wght]_customized.ttf"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found in the current directory.")
        return

    print(f"Step 1: Shifting the default wght axis to {wght}...")
    font = TTFont(input_path)
    font = instancer.instantiateVariableFont(font, {"wght": (200, wght, 900)})

    print("Step 2: Analyzing GSUB and backing character variants into defaults...")
    features_to_bake = {"cv01", "cv03", "cv04", "cv07", "cv09", "cv11", "cv15"}

    if "GSUB" in font:
        gsub = font["GSUB"].table
        cmap = font["cmap"].getBestCmap()

        # Store original forward mappings (original_glyph_name -> alternative_glyph_name)
        forward_mappings = {}

        # Track which lookups belong to our target cvXX features so we can invert them later
        target_lookups = set()

        # 1. Identify and extract mappings for the requested cvXX tags
        for feature_record in gsub.FeatureList.FeatureRecord:
            if feature_record.FeatureTag in features_to_bake:
                feature = feature_record.Feature
                for lookup_idx in feature.LookupListIndex:
                    target_lookups.add(lookup_idx)
                    lookup = gsub.LookupList.Lookup[lookup_idx]

                    if lookup.LookupType == 1:  # Single Substitution
                        for subtable in lookup.SubTable:
                            for orig_glyph, alt_glyph in subtable.mapping.items():
                                forward_mappings[orig_glyph] = alt_glyph

        if forward_mappings:
            # 2. Update the default unicode character map (cmap) to make alternates the default
            for codepoint, glyph_name in list(cmap.items()):
                if glyph_name in forward_mappings:
                    alt_glyph = forward_mappings[glyph_name]
                    cmap[codepoint] = alt_glyph
                    print(
                        f"  -> Remapped Unicode codepoint: {glyph_name} -> {alt_glyph}"
                    )

            print(
                "Step 3: Inverting GSUB lookup tables to make cvXX toggles reverse the effect..."
            )
            # 3. Invert the GSUB lookup tables for targeted cvXX features.
            # Instead of 'Replace Default with Alternate', it becomes 'Replace Alternate with Default'.
            for lookup_idx in target_lookups:
                lookup = gsub.LookupList.Lookup[lookup_idx]
                if lookup.LookupType == 1:
                    for subtable in lookup.SubTable:
                        # Create an inverted mapping dictionary
                        inverted_subtable_mapping = {}
                        for orig_glyph, alt_glyph in list(subtable.mapping.items()):
                            # Swap keys and values to reverse the behavior
                            inverted_subtable_mapping[alt_glyph] = orig_glyph

                        # Replace the old mapping structure with the inverted one
                        subtable.mapping = inverted_subtable_mapping
            print("  -> GSUB substitution rules successfully reversed.")
        else:
            print(
                "  Warning: No substitution rules for the specified cvXX features were found in the GSUB table."
            )
    else:
        print("  Error: Font does not contain a GSUB table.")

    print("Step 4: Aligning fvar table named instances to the new default...")
    if "fvar" in font:
        for instance in font["fvar"].instances:
            if instance.coordinates.get("wght") == 400:
                instance.coordinates["wght"] = wght
                print(
                    f"  -> Updated fvar table instance coordinates from 400 to {wght}."
                )

    font.save(output_path)
    font.close()
    print(f"\nSuccess! Generated file: {output_path}")


if __name__ == "__main__":
    patch_reddit_mono()
