import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kubetpl",
    version="1.0.0",
    author="Grauer W01f",
    author_email="grauerwf@gmail.com",
    description="A templater for kubernetes resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grauerwf/kubtemplate",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'kubtemplate=kubtemplate.kubtemplate:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
