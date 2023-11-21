# This file, and all of it's code, is licensed under the MIT License.
# See LICENSE.
# Copyright (c) 2023 irixaligned

import sys
import subprocess
import hashlib
import xml.etree.ElementTree as ET
import os

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_fastboot():
    if "--fastboot-path" in sys.argv:
        index = sys.argv.index("--fastboot-path") + 1
        if index < len(sys.argv):
            path = sys.argv[index]
            if os.path.isfile(path):
                return path
            else:
                print(f"Error: Specified fastboot binary not found at {path}")
                sys.exit(1)

    if os.path.isfile("fastboot"):
        return os.path.join(".", "fastboot")

    if os.name == 'posix':
        try:
            subprocess.run(["fastboot", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return "fastboot"
        except subprocess.CalledProcessError:
            pass

    return None

def check_fastboot_device(fastboot_path):
    try:
        result = subprocess.run([fastboot_path, "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        output = result.stdout

        can_flash = False if "no permissions" in output.lower() or not output.strip() else True
        fastbootd = True if "fastbootd" in output.lower() else False

        return can_flash, fastbootd
    except subprocess.CalledProcessError as e:
        print(f"Error checking fastboot devices: {e}")
        sys.exit(1)

def main():
    print("Savior When Absolutely Trashed (SWAT)")
    print("a tiny system rescue utility for Motorola devices")
    print("irixaligned (& contributors) 2023\n")

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} flashfile.xml [--fastboot-path /path/to/fastboot] [--ignore-md5] [--disable-avb]")
        print("Options:")
        print("  --fastboot-path: Specify an alternate fastboot binary.")
        print("  --ignore-md5: Disable verification of images against their hashes.")
        print("  --disable-avb: Disable Android Verified Boot if your device supports it.")
        sys.exit(1)

    flashfile = sys.argv[1]
    fastboot_path = find_fastboot()
    ignore_md5 = False
    disable_avb = False

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--ignore-md5":
            ignore_md5 = True
        elif sys.argv[i] == "--disable-avb":
            disable_avb = True

    if not fastboot_path:
        print("Error: Fastboot binary not found. Please specify the path using --fastboot-path.")
        sys.exit(1)

    if not os.path.isfile(flashfile):
        print(f"Error: XML file '{flashfile}' not found.")
        sys.exit(1)

    flashfile_dir = os.path.dirname(os.path.abspath(flashfile))

    can_flash, is_fastbootd = check_fastboot_device(fastboot_path)
    
    if not can_flash:
        print(f"Error: Either the device is not connected, or you have insufficient permissions to access it.\nConsider running the script as admin/root or checking if you're in the plugdev group on Linux.")
        sys.exit(1)

    if is_fastbootd:
        print(f"!!! WARNING !!!\nThis device is booted via fastbootd rather than the bootloader fastboot.\nfastbootd is generally more reliable, but not in circumstances where you're doing system critical reflashes like the ones this tool does.\nIt is probably a bad idea to continue. Zero warranty. DO NOT COMPLAIN.\n")

    tree = ET.parse(flashfile)
    root = tree.getroot()

    print(f"Fastboot path: {fastboot_path}")
    print(f"Flashfile: {flashfile}")
    print(f"Ignore MD5: {ignore_md5}")
    print(f"Disable AVB: {disable_avb}")
    print(f"Is fastbootd active: {is_fastbootd}\n")
    print(f"Please ensure your bootloader is unlocked.\nThere is no proper way to check for that on the software's end,\nand your flashing may fail (although not in any destructive way) if not.\n")

    proceed = input("ALL OF YOUR DATA WILL BE ERASED. Do you want to proceed? (y/n): ").lower()

    if proceed != "y":
        print("Exiting.")
        sys.exit(0)

    for step in root.findall(".//steps/step"):
        md5 = step.get("MD5")
        filename = step.get("filename")
        operation = step.get("operation")
        partition = step.get("partition")
        var = step.get("var")

        canon_filename = os.path.join(flashfile_dir, filename) if filename else None

        if md5 and filename and not ignore_md5:
            calculated_md5 = calculate_md5(canon_filename)
            if calculated_md5 != md5:
                print(f"Error: MD5 verification failed for {filename}")
                sys.exit(1)
            else:
                print(f"MD5 signature passes for {filename}")

        command = f"{fastboot_path} {operation}"

        if operation in ["flash", "erase"]:
            command += f" {partition}"
            if operation == "flash":
                if disable_avb and ("vbmeta" in partition):
                    command += " --disable-verity --disable-verification"
                command += f" \"{canon_filename}\""
        else:
            command += f" {var}" if var else ""

        if operation in ["flash", "erase"]:
            if operation == "flash":
                print(f"Flashing: \"{filename}\" to \"{partition}\"")
            else:
                print(f"Erasing: \"{partition}\"")
        else:
            if var:
                print(f"Operation: \"{operation}\" performed with argument \"{var}\"")
            else:
                print(f"Operation: \"{operation}\" performed")

        print(f"(command: {command})")

        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            if "FAILED" in result.stdout:
                print(f"Error: Command failed: {result.stdout}")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            sys.exit(1)

    reboot = input("Flashed successfully! Do you want to reboot? (y/n): ").lower()
    if reboot == "y":
        subprocess.run(f"{fastboot_path} reboot", shell=True)

if __name__ == "__main__":
    main()
