from setuptools import find_packages, setup

package_name = 'services_py'

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
            'add_two_ints_server = services_py.add_two_ints_server:main',
            'add_two_ints_client_no_oop = services_py.add_two_ints_client_no_oop:main',
            'add_two_ints_client = services_py.add_two_ints_client:main',
        ],
    },
)
