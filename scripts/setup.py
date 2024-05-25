import site
import os


def add_package_to_site_packages(target_directory):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abs_path = os.path.abspath(os.path.join(project_root, target_directory))
    site_packages_path = site.getsitepackages()

    for sp_path in site_packages_path:
        pth_file_path = os.path.join(sp_path, 'custom_package_paths.pth')
        with open(pth_file_path, 'a') as file:
            file.write(abs_path + '\n')

    for root, dirs, files in os.walk(abs_path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if "__init__.py" in os.listdir(dir_path):
                with open(pth_file_path, 'a') as file:
                    file.write(dir_path + '\n')

    print(f"Added {abs_path} to site-packages .pth files in: {site_packages_path}")


if __name__ == "__main__":
    add_package_to_site_packages("src")
