import setuptools

from tesaurus.tesaurus import __author__, __author_mail__, __version__

with open("README.md", "r", encoding="utf-8") as fp:
    long_desc = fp.read()

setuptools.setup(
    name="tesaurus",
    version=__version__,
    description="Sebuah modul Python untuk mengambil informasi Tesaurus dari Tesaurus Tematis Kemdikbud",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__author_mail__,
    license="MIT",
    packages=setuptools.find_packages(),
    url="https://github.com/noaione/tesaurus-python",
    install_requires=["beautifulsoup4", "requests", "aiohttp"],
    keywords=["tesaurus", "lema", "bahasa", "indonesia", "scraper", "async"],
    entry_points={"console_scripts": ["tesaurus=tesaurus.perintah:cli"]},
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Indonesian",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
)
