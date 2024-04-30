import site
import os


def add_package_to_site_packages(target_directory):
    # Convert the target directory to an absolute path
    abs_path = os.path.abspath(target_directory)

    # Get the path to the site-packages directory
    site_packages_path = site.getsitepackages()

    # For systems with multiple site-packages directories (e.g., virtual environments)
    # we add the path to all site-packages found
    for sp_path in site_packages_path:
        # Construct the full path for the .pth file
        pth_file_path = os.path.join(sp_path, 'custom_package_paths.pth')

        # Write the absolute path to the .pth file
        with open(pth_file_path, 'a') as file:
            file.write(abs_path + '\n')

    print(f"Added {abs_path} to site-packages .pth files in: {site_packages_path}")


if __name__ == "__main__":
    add_package_to_site_packages("lib")