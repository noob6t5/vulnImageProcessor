import os,socket,subprocess

flag_path = "./flag.txt"
upload_folder = "./upload"


with open(flag_path, "w") as f:
    f.write("flag{RTLO_Key_jayHo}")

def jpg_check(filename):
    return filename.lower().endswith(".jpg")

def extract_metadata(file_path):
    try:
        command = f"exiftool {file_path}"
        output = subprocess.check_output(command, shell=True).decode()
        return output
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None

def rtlo_check(metadata):
    RTLO = "\u202E"
    return RTLO in metadata


def maybe_danger(metadata):
    print("RTLO..")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 0))  
        s.listen()
        port = s.getsockname()[1]
        print(f"Netcat started on port {port}...")

        print(f"DO:  nc localhost {port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connection established with {addr}")
            data = conn.recv(1024).decode().strip()
            if data == "whoami":
                with open(flag_path, "r") as f:
                    flag = f.read().strip()
                    conn.sendall(flag.encode())
            else:
                conn.sendall(b"Only 'whoami ' will work.")

def upload_image():
    filename = input(
        "Enter the name of the image to upload: "
    ).strip()
    file_path = os.path.join(upload_folder, filename)
    if not jpg_check(filename):
        print("Error: Only .jpg files are allowed.")
        return
    if not os.path.exists(file_path):
        print(f"Error: {filename} does not exist in the upload folder.")
        return

    print(f"Processing {filename}...")
    metadata = extract_metadata(file_path)

    if metadata is None:
        print("Error processing image metadata.")
        return
    if rtlo_check(metadata):
        maybe_danger(metadata)
    else:
        print("No RTLO character. But You found Lollipop:)")


def delete_image():
    filename = input("Enter the name of the image to delete: ").strip()
    file_path = os.path.join(upload_folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{filename} deleted successfully.")
    else:
        print(f"{filename} does not exist in the upload folder.")


def main():
    print("\tVulnerable Image Uploader/Processor")
    print("Please use RTLO method for image payload.")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    while True:
        print("\n----------------")
        print("\tOptions")
        print("1. Upload Image")
        print("2. Delete Image")
        print("3. Exit")
        choice = input("Choose froma above : ").strip()

        if choice == "1":
            upload_image()
        elif choice == "2":
            delete_image()
        elif choice == "3":
            print("bye")
            break
        else:
            print("Check Options")

if __name__ == "__main__":
    main()
