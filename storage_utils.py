# Face hash local storage utility (Micro:bit file operation)
# Function: Save hash to local file, read stored hash list, no raw face data stored
from microbit import *

def save_face_hash(face_hash):
    """
    Save face hash to local file (face_hashes.txt), one hash per line
    :param face_hash: Generated face hash string
    :return: True if saved successfully, False if failed
    """
    try:
        # Open file in append mode (data not lost after power off)
        with open("face_hashes.txt", "a") as f:
            f.write(f"{face_hash}\n")
        display.scroll("Hash Saved")  # LED prompt for successful save
        return True
    except Exception as e:
        display.scroll("Save Err")
        print(f"Hash save failed: {e}")  # Serial port output error log (for debugging)
        return False

def load_stored_hashes():
    """
    Read all face hashes stored locally and return hash list
    :return: List of stored hashes (e.g., ["hash1", "hash2"])
    """
    stored_hashes = []
    try:
        # Read file, create empty file if not exists
        with open("face_hashes.txt", "r") as f:
            lines = f.readlines()
            # Remove blank lines and newlines, organize into pure hash list
            stored_hashes = [line.strip() for line in lines if line.strip()]
    except OSError:
        # Create empty file when file does not exist
        with open("face_hashes.txt", "w") as f:
            pass
    return stored_hashes

def save_hash_to_num(hash_str, num):
    """
    Save the binding relationship between hash and number (display corresponding number after authentication)
    :param hash_str: Face hash
    :param num: Bound number (1-3)
    """
    try:
        with open("hash_to_num.txt", "a") as f:
            f.write(f"{hash_str}:{num}\n")
        return True
    except Exception as e:
        print(f"Hash-number binding save failed: {e}")
        return False

def load_hash_to_num():
    """Read the binding relationship between hash and number, return dictionary"""
    hash_to_num = {}
    try:
        with open("hash_to_num.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                h, n = line.strip().split(":", 1)
                hash_to_num[h] = int(n)
    except OSError:
        with open("hash_to_num.txt", "w") as f:
            pass
    return hash_to_num
