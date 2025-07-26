import base64

def get_base64_of_bin_file(bin_file):
    """Reads a binary file and returns its base64 encoded string."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None
