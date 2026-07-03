from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_robot'

setup(
    name='my_robot',
    version='0.0.0',
    packages=['my_robot'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/my_robot']),
        ('share/my_robot', ['package.xml']),
        # Ensure these lines exist:
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')), #added extra for new world
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='manju',
    maintainer_email='1ms23me043@msrit.edu',
    description='Differential drive robot simulation in Gazebo Harmonic',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
