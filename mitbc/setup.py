#!/usr/bin/env python3
import os
import subprocess
import sys

def check_rabbitmq():
    try:
        # Check if RabbitMQ is installed
        subprocess.run(['rabbitmqctl', 'status'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("RabbitMQ is installed.")
        return True
    except FileNotFoundError:
        print("RabbitMQ is not installed.")
        return False
    except subprocess.CalledProcessError:
        print("RabbitMQ is installed but not running.")
        return True  # RabbitMQ might be installed but not running

def install_rabbitmq():
    print("Installing RabbitMQ...")
    try:
        # Update system and install RabbitMQ
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'rabbitmq-server'], check=True)
        print("RabbitMQ installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

def enable_and_start_rabbitmq():
    print("Enabling and starting RabbitMQ service...")
    try:
        # Enable and start RabbitMQ service
        subprocess.run(['sudo', 'systemctl', 'enable', 'rabbitmq-server'], check=True)
        subprocess.run(['sudo', 'systemctl', 'start', 'rabbitmq-server'], check=True)
        print("RabbitMQ service started and enabled.")
    except subprocess.CalledProcessError as e:
        print(f"Error during enabling or starting RabbitMQ: {e}")
        sys.exit(1)

def main():
    if not check_rabbitmq():
        install_rabbitmq()
        enable_and_start_rabbitmq()
    else:
        print("Ensuring RabbitMQ service is running...")
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'rabbitmq-server'], check=True)
            print("RabbitMQ service is running.")
        except subprocess.CalledProcessError:
            print("Failed to start RabbitMQ service.")
            sys.exit(1)



from setuptools import setup, find_packages

# get key package details from py_pkg/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'py_pkg', '__version__.py')) as f:
#    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open("README.md", "r") as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name="mitb",
    description="Message In the Bottle manages a variety of enc/decrypt methods local and remote",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="0.9",
    author="nullvex",
    author_email="info@perpetual.media",
    url="__url__",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7.*",
    install_requires=["numpy", "requests", "rsa", "pycryptodome", "tqdm", "paramiko", "requests", "argparse", "black", "pika", "pyjwt"],
    license="__license__",
    zip_safe=False,
    entry_points={
        "console_scripts": ["mitb = mitb.__main__:mitb_init"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="package development template",
)

if __name__ == "__main__":
    main()
