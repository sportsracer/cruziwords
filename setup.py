import setuptools

setuptools.setup(
    name="cruziwords",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    package_data={
        "cruziwords.examples": ["european_capitals.csv"],
        "cruziwords.view": ["template.html"],
    },
    description="Crossword puzzle generator",
    author="Steffen Wenz",
    url="https://github.com/sportsracer/cruziwords",
    install_requires=[
        "mako",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={"console_scripts": ["cruziwords=cruziwords.__main__:main"]},
)
