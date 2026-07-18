import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer


def patch_font(input_path, output_path, wght, features_to_bake):
    """
    input_path: path to the source variable font (.ttf)
    output_path: path to write the patched font to
    wght: new default wght value (int)
    features_to_bake: iterable of OpenType feature tags to bake as default,
        e.g. {"ss02", "ss07"}
    """
    features_to_bake = set(features_to_bake)

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return False

    font = TTFont(input_path)

    # --- Step 0: Read the font's real wght axis range instead of guessing it ---
    fvar = font["fvar"]
    wght_axis = next(a for a in fvar.axes if a.axisTag == "wght")
    axis_min, axis_max = wght_axis.minValue, wght_axis.maxValue
    old_default = wght_axis.defaultValue
    print(
        f"Step 0: Detected wght axis: min={axis_min}, default={old_default}, max={axis_max}"
    )

    print(f"Step 1: Shifting the default wght axis to {wght}...")
    font = instancer.instantiateVariableFont(font, {"wght": (axis_min, wght, axis_max)})

    print("Step 2: Analyzing GSUB and backing character variants into defaults...")

    if "GSUB" in font:
        gsub = font["GSUB"].table
        cmap = font["cmap"].getBestCmap()

        # Store original forward mappings (original_glyph_name -> alternative_glyph_name)
        forward_mappings = {}

        # Track which lookups belong to our target features so we can invert them later
        target_lookups = set()

        # 1. Identify and extract mappings for the requested feature tags
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
                "Step 3: Inverting GSUB lookup tables to make feature toggles reverse the effect..."
            )
            # 3. Invert the GSUB lookup tables for targeted features.
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
                "  Warning: No substitution rules for the specified features were found in the GSUB table."
            )
    else:
        print("  Error: Font does not contain a GSUB table.")

    print("Step 4: Aligning fvar table named instances to the new default...")
    if "fvar" in font:
        for instance in font["fvar"].instances:
            if instance.coordinates.get("wght") == old_default:
                instance.coordinates["wght"] = wght
                print(
                    f"  -> Updated fvar instance coordinates from {old_default} to {wght}."
                )

    print(
        "Step 5: Updating OS/2.usWeightClass so non-variable-aware apps pick it up..."
    )
    if "OS/2" in font:
        old_weight_class = font["OS/2"].usWeightClass
        font["OS/2"].usWeightClass = wght
        print(f"  -> Updated OS/2.usWeightClass from {old_weight_class} to {wght}.")

    print("Step 6: Checking STAT table for a stale default AxisValue...")
    if "STAT" in font and font["STAT"].table.AxisValueArray:
        for av in font["STAT"].table.AxisValueArray.AxisValue:
            # Format 1/3 AxisValue records carry a single .Value we care about here.
            value = getattr(av, "Value", None)
            if value == old_default:
                av.Value = wght
                print(f"  -> Updated STAT AxisValue from {old_default} to {wght}.")

    font.save(output_path)
    font.close()
    print(f"\nSuccess! Generated file: {output_path}")
    return True
