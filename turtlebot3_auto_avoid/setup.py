from setuptools import setup

package_name = 'turtlebot3_auto_avoid'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mithill Prabhu',
    maintainer_email='psmithill27@gmail.com',
    description='TurtleBot3 LiDAR obstacle avoidance and SLAM map saving for ROS 2',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'auto_avoid = turtlebot3_auto_avoid.auto_avoid:main',
            'map_saver = turtlebot3_auto_avoid.map_saver:main',
        ],
    },
)

