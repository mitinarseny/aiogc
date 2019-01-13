import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiogc",
    version="0.1.4",
    author="Arseny Mitin",
    author_email="mitinarseny@gmail.com",
    description="Async Google Calendar API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mitinarseny/aiogc",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp>=3.5.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
