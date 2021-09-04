import setuptools

setuptools.setup(
    name="cruziwords",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    description="Crossword puzzle generator",
    author="Steffen Wenz",
    url="https://github.com/sportsracer/cruziwords",
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ]
)
