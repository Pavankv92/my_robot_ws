from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pavankv',
    maintainer_email='pavankv92@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'first_node = my_py_pkg.first_node:main',
            'my_publisher = my_py_pkg.my_publisher:main',
            'my_subscriber = my_py_pkg.my_subscriber:main',
            'add_two_ints_server = my_py_pkg.add_two_ints_server:main',
            'add_two_ints_client_no_oop = my_py_pkg.add_two_ints_client_no_oop:main',
            'add_two_ints_client = my_py_pkg.add_two_ints_client:main',
            'hardware_status_publisher = my_py_pkg.hardware_status_publisher:main',
            'param_publisher = my_py_pkg.param_publisher:main',


        ],
    },
)
