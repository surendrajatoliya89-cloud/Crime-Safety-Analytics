import os
import zipfile

desktop_dir = r"C:\Users\Admin\OneDrive\Desktop"
project_dir = r"C:\Users\Admin\OneDrive\Desktop\Crime-Safety-Analytics"
zip_output = os.path.join(desktop_dir, "Crime_Analytics_Deploy_Package.zip")

print("Packaging project for deployment...")
exclude_dirs = {"venv", ".git", "__pycache__"}
exclude_extensions = {".pyc", ".log"}

with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_dir):
        # Skip excluded dirs
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in exclude_extensions) or file.endswith(".exe"):
                continue
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, project_dir)
            zipf.write(abs_path, rel_path)

print(f"Deployment ZIP package created successfully at:\n  {zip_output}")
