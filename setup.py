from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="download_oscar",
    packages=["download_oscar"],
    version="1.1",
    license="MIT",
    description="Downloading all files of a language from the OSCAR (Open Super-large Crawled Aggregated coRpus)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="xamm",
    author_email="xamm.apps@gmail.com",
    url="https://github.com/xamm/download_oscar",
    download_url="https://pypi.org/project/download-oscar/",
    keywords=[
        "nlp",
        "dataset",
        "automation",
    ],
    install_requires=[
        "beautifulsoup4",
        "html5lib",
        "PySimpleGUI",
        "requests",
        "tqdm",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": ["dodc=download_oscar.dod:main", "dodg=download_oscar.dod_gui:main"],
    },
)
