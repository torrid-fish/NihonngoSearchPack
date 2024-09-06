from setuptools import setup, find_packages

setup(
    name='NihonngoSearchPack',          # Name of your project
    version='0.1',                     # Version of your project
    description='A package that supports to search a lot of stuff.', # Short description of your project
    author='torrid-fish',                # Author's name
    author_email='justinwu6900942@gmail.com',  # Author's email
    url='https://github.com/torrid-fish/NihonngoSearchPack',  # URL for your project (e.g., GitHub)
    packages=find_packages(),          # Automatically find all packages
    install_requires=[                 # List of dependencies (if any)
        'requests',  # Example dependency
        'bs4'
    ],
    classifiers=[                      # Metadata for the package
        
    ],
    python_requires='>=3.6',           # Specify supported Python versions
)

