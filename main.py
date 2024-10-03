import os
import json
import re
import argparse
from typing import Dict, List, Any

def parse_defconfig(defconfig_path: str) -> Dict[str, str]:
    """Parse the defconfig file to extract required configuration values."""
    config_data: Dict[str, str] = {}
    with open(defconfig_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                config_data[key] = value
    return config_data

def extract_usb_id(config_data: Dict[str, str]) -> List[str]:
    """Extract USBID list from config data."""
    vendor_id = config_data.get('CONFIG_CDCACM_VENDORID', '').strip().strip('"')
    product_id = config_data.get('CONFIG_CDCACM_PRODUCTID', '').strip().strip('"')
    usb_ids = []
    if vendor_id and product_id:
        usb_id = f"{vendor_id}/{product_id}"
        usb_ids.append(usb_id)
    return usb_ids

def main() -> None:
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process the base directory.')
    parser.add_argument('base_dir', nargs='?', default='./boards',
                        help='The base directory to process')
    args = parser.parse_args()
    base_dir = args.base_dir

    # Initialize the list to hold the final JSON entries
    final_entries: List[Dict[str, Any]] = []

    # Walk through the directory structure
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == 'firmware.prototype':
                firmware_prototype_path = os.path.join(root, file)
                # Parse the firmware.prototype file
                with open(firmware_prototype_path, 'r') as f:
                    firmware_data = json.load(f)

                # Extract 'board_id' and other relevant data
                board_id = firmware_data.get('board_id')
                description = firmware_data.get('description', '')
                summary = firmware_data.get('summary', '')

                # Find the corresponding 'defconfig' files
                defconfig_paths: List[str] = []
                for dirpath, dirnames, filenames in os.walk(root):
                    for fname in filenames:
                        if fname == 'defconfig':
                            defconfig_paths.append(os.path.join(dirpath, fname))

                # If defconfig file found, parse it
                usb_ids = []
                vendor_str = ''
                for defconfig_path in defconfig_paths:
                    config_data = parse_defconfig(defconfig_path)
                    usb_id_list = extract_usb_id(config_data)
                    usb_ids.extend(usb_id_list)
                    vendor_str_candidate = config_data.get('CONFIG_CDCACM_VENDORSTR', '').strip().strip('"')
                    if vendor_str_candidate:
                        vendor_str = vendor_str_candidate  # Overwrite with last found

                # Construct 'firmware_name' from folder structure
                parts = root.split(os.sep)
                try:
                    boards_index = parts.index('boards')
                    firmware_name_parts = parts[boards_index + 1:]
                    firmware_name = '_'.join(firmware_name_parts)
                except ValueError:
                    firmware_name = '_'.join(parts)

                # Build the 'bootloader_str' (we can use firmware_name and vendor_str)
                bootloader_str = [firmware_name]
                if vendor_str:
                    bootloader_str.append(vendor_str)

                # Build the final JSON entry
                entry: Dict[str, Any] = {
                    'board_id': board_id,
                    'platform': firmware_name + '_default',
                    'USBID': usb_ids,
                    'brand_name': vendor_str,
                    'manufacturer': vendor_str,
                    'description': description,
                    'summary': summary,
                    'bootloader_str': bootloader_str,
                }

                final_entries.append(entry)

    # Output the final JSON
    output_json = json.dumps(final_entries, indent=2)
    print(output_json)

if __name__ == '__main__':
    main()
