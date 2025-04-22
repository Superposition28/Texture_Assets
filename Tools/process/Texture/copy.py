import os
import shutil
import sys
import configparser

def read_config(file_path: str) -> str:
    """Reads and displays the contents of a configuration file."""
    config = configparser.ConfigParser()
    config.read(file_path)

    txd_dir = config.get('Directories', 'txd_dir')
    png_dir = config.get('Directories', 'png_dir')

    return txd_dir, png_dir


txd_dir, png_dir = read_config(r"txdConf.ini")
print(f"Source Root: {txd_dir}")
print(f"Destination Root: {png_dir}")

if not os.path.exists(txd_dir):
    print(f"Source directory '{txd_dir}' does not exist. Exiting.", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(png_dir):
    print(f"Destination directory '{png_dir}' does not exist. Creating...")
    os.makedirs(png_dir, exist_ok=True)

txd_dir = os.path.abspath(txd_dir)

for dirpath, _, filenames in os.walk(txd_dir):
    for filename in filenames:
        if filename.lower().endswith('.png'):
            full_file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(full_file_path, txd_dir)
            print(f"Relative Path: {relative_path}")

            destination_path = os.path.join(png_dir, relative_path)
            destination_dir = os.path.dirname(destination_path)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir, exist_ok=True)

            shutil.copy2(full_file_path, destination_path)
