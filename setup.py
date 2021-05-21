import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vbox-operator",
    version="0.0.3",
    author="Humoud Al Saleh",
    author_email="humoud@corpse.io",
    description="An interactive command line interface for VirtualBox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Humoud/vbox-operator",
    project_urls={
        "Bug Tracker": "https://github.com/Humoud/vbox-operator/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    keywords='virtualbox vbox operator',  # Optional
    install_requires=['prompt-toolkit', 'Pygments'],
    entry_points={
        'console_scripts': 'vbox-operator = vbox_operator.__main__:main'
    }
)