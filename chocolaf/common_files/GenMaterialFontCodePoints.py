import re

def to_camel(name):
    # Prefix names starting with a digit (e.g., 3d_rotation -> Icon3dRotation)
    parts = name.split("_")
    camel = "".join(p.capitalize() for p in parts)
    return f"Icon{camel}" if camel[0].isdigit() else camel

with open("MaterialIcons-Regular.codepoints") as f:
    lines = [line.strip().split() for line in f if line.strip()]

with open("MaterialIconNames.h", "w") as out:
    out.write("#pragma once\n\n")
    out.write("namespace IconFont::Icons {\n")
    for name, hex_val in lines:
        var_name = to_camel(name)
        out.write(f"    inline constexpr char32_t {var_name:<30} = 0x{hex_val}; // {name}\n")
    out.write("}\n")

print(f"Generated MaterialIconNames.h with {len(lines)} glyphs successfully.")
