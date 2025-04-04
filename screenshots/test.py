import os

# Directory where your screenshots are stored
screenshots_dir = r"C:\Users\TAMANG\Documents\GitHub\Enforcement-Agents\screenshots"

# List all files in the screenshots directory
all_files = os.listdir(screenshots_dir)

# Create a mapping from zero-padded to non-padded filenames
rename_map = {}
for filename in all_files:
    if filename.startswith("results_with_ea_run_") or filename.startswith("results_with_2_ea_run_"):
        base, ext = os.path.splitext(filename)
        parts = base.split("_")
        run_number_str = parts[-1]  # last part should be something like '001'
        try:
            run_number_int = int(run_number_str)
            new_filename = "_".join(parts[:-1]) + f"_{run_number_int}{ext}"
            rename_map[filename] = new_filename
        except ValueError:
            pass  # skip files that don't have a numeric suffix

# Apply the renaming
for old_name, new_name in rename_map.items():
    os.rename(os.path.join(screenshots_dir, old_name), os.path.join(screenshots_dir, new_name))

# Show sample of renamed files
list(rename_map.items())[:10]
