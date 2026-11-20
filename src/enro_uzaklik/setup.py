from setuptools import find_packages, setup

package_name = 'enro_uzaklik'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ENRO Aday',
    maintainer_email='aday@enro.local',
    description='ENRO hedef uzakligi kontrol servis ve istemci dugumleri',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'uzaklik_sunucu = enro_uzaklik.uzaklik_sunucu:main',
            'uzaklik_istemci = enro_uzaklik.uzaklik_istemci:main',
        ],
    },
)
