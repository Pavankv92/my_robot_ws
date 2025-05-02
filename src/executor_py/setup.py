from setuptools import find_packages, setup

package_name = 'executor_py'

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
            'number_publisher_with_executor = executor_py.number_publisher_with_executor:main',
            'single_threaded_executor = executor_py.single_threaded_executor:main',
            'multi_threaded_executor = executor_py.multi_threaded_executor:main',
            'multiple_nodes_in_executor = executor_py.multiple_nodes_in_executor:main',
            'multiple_nodes_in_multithreaded_executor = executor_py.multiple_nodes_in_multithreaded_executor:main',
        ],
    },
)
