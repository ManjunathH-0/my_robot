from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files
        (os.path.join('share' , package_name, 'launch'),glob(os.path.join('launch','*.[pxt][yma]*'))),
        # Include all SDF files    
        (os.path.join('share' , package_name, 'models','diff_drive_robot'),glob(os.path.join('models','diff_drive_robot','*'))),
        # Include all Gazebo worlds
        (os.path.join('share', package_name , 'worlds'),glob(os.path.join('worlds','*.sdf'))),
         
        

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='manju',
    maintainer_email='1ms23me043@msrit.edu',
    description='Differential drive robot simulation in Gazebo Harmonic',
    license='Apache-2.0',
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
