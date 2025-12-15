# Micro:bit face recognition robot main program
# Function: Serial communication to receive face features, hash generation/storage/comparison, LED display, key interaction
from microbit import *
from hash_utils import generate_face_hash, compare_face_hash
from storage_utils import save_face_hash, load_stored_hashes, save_hash_to_num, load_hash_to_num

# ---------------------- Configuration Items ----------------------
# Serial port configuration (communication with ESP32-CAM, baud rate 9600)
uart.init(baudrate=9600, tx=pin0, rx=pin1)
# LED digital display dot matrix (5×5 matrix)
NUMBERS = {
    1: [[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,1,0]],
    2: [[0,1,1,1,0],[1,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,1,1,1]],
    3: [[0,1,1,1,0],[1,0,0,0,1],[0,0,1,1,0],[1,0,0,0,1],[0,1,1,1,0]]
}

# ---------------------- Basic Utility Functions ----------------------
def display_number(num):
    """Display number (1-3) on Micro:bit LED matrix"""
    if num not in NUMBERS:
        display.clear()
        return
    for y in range(5):
        for x in range(5):
            display.set_pixel(x, y, 9 if NUMBERS[num][y][x] else 0)

def receive_face_feature():
    """Receive face feature string from ESP32-CAM (agreed format: face_feature:xxx)"""
    if uart.any():
        data = uart.readline().decode().strip()
        if data.startswith("face_feature:"):
            return data.split(":", 1)[1]  # Extract pure feature string
    return None

# ---------------------- Core Business Logic ----------------------
def enroll_face(num):
    """
    Enroll face: collect features → generate hash → store hash (no raw data) → bind number
    :param num: Bound number (1-3)
    """
    display.scroll(f"Enroll {num}")
    sleep(1000)
    
    # Wait to receive face features
    face_feature = None
    while not face_feature:
        face_feature = receive_face_feature()
        display.set_pixel(2, 2, 9)  # Blink middle LED to prompt collection
        sleep(500)
        display.set_pixel(2, 2, 0)
        sleep(500)
    
    # Generate hash (core: only store hash, discard raw features)
    face_hash = generate_face_hash(face_feature)
    print(f"Generated Hash: {face_hash}")  # Serial port log (for debugging)
    
    # Store hash and binding relationship
    if save_face_hash(face_hash) and save_hash_to_num(face_hash, num):
        display_number(num)  # Display bound number
        sleep(2000)
    display.clear()

def authenticate_face():
    """
    Face authentication: collect real-time features → generate hash → compare with stored hashes → display result
    :return: Bound number if authentication passed, None if failed
    """
    display.scroll("Auth")
    sleep(1000)
    
    # Wait to receive real-time face features
    face_feature = None
    while not face_feature:
        face_feature = receive_face_feature()
        display.set_pixel(2, 2, 9)
        sleep(300)
        display.set_pixel(2, 2, 0)
        sleep(300)
    
    # Generate real-time hash (no raw features stored)
    input_hash = generate_face_hash(face_feature)
    print(f"Real-time Hash: {input_hash}")
    
    # Load stored hashes and binding relationships
    stored_hashes = load_stored_hashes()
    hash_to_num = load_hash_to_num()
    
    # Hash comparison
    if compare_face_hash(input_hash, stored_hashes):
        num = hash_to_num.get(input_hash, 0)
        display_number(num)
        uart.write("auth_pass\n")  # Send authentication success command to ESP32-CAM
        sleep(3000)
        return num
    else:
        display.scroll("Fail")
        uart.write("auth_fail\n")
        sleep(2000)
        return None

# ---------------------- Main Loop (Key Interaction) ----------------------
# Key logic: Button A enrolls face 1, Button B enrolls face 2, Buttons A+B authenticate
while True:
    if button_a.is_pressed() and not button_b.is_pressed():
        enroll_face(1)
    elif button_b.is_pressed() and not button_a.is_pressed():
        enroll_face(2)
    elif button_a.is_pressed() and button_b.is_pressed():
        authenticate_face()
    display.clear()
    sleep(500)
