import os

path = r"C:\Users\SANTHEESH\Downloads\pgvector-0.8.0-pg18-windows-x64"
print(f"Path: {path} exists: {os.path.exists(path)}")
if os.path.exists(path):
    print("Contents:")
    for root, dirs, files in os.walk(path):
        for f in files:
            print(os.path.join(root, f))
