# Face hash encryption and comparison utility class
# Function: Generate SHA-256 hash for face features, compare real-time hash with stored hashes
import hashlib

def generate_face_hash(face_feature_str):
    """
    Generate SHA-256 hash for face feature string (irreversible, only store hash not raw data)
    :param face_feature_str: Face feature string transmitted by ESP32-CAM (e.g., spliced feature vector)
    :return: 64-bit hexadecimal hash string
    """
    # Convert string to byte stream (hash function requires bytes input)
    feature_bytes = face_feature_str.encode("utf-8")
    # Calculate SHA-256 hash
    hash_object = hashlib.sha256(feature_bytes)
    face_hash = hash_object.hexdigest()
    return face_hash

def compare_face_hash(input_hash, stored_hash_list):
    """
    Compare real-time face hash with stored hash list
    :param input_hash: Real-time generated face hash during authentication
    :param stored_hash_list: List of authorized face hashes stored locally
    :return: True (match success/authentication passed), False (match failed/authentication rejected)
    """
    return input_hash in stored_hash_list
