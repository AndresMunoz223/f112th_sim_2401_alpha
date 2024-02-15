from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'wall_following_alpha'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        (os.path.join('share', package_name), glob('config/*.yaml')),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='epsdelta',
    maintainer_email='andresfmc223@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
    'break = wall_following_alpha.break:main',
    'dist_finder_alpha = wall_following_alpha.distance_finder_alpha:main',
    'control_alpha = wall_following_alpha.control_alpha:main',
    'gap_control_alpha = wall_following_alpha.gap_control_alpha:main',
    ],
},
)
