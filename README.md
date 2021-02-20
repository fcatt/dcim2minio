# dcim2minio
Backup digital pictures from a DCIM directory to a MinIO object storage

This is my first project with Python. I had a week-long "Object programming in Python" training session fall 2020 and I hadn't yet (february 2021) put my knowledge into practice.

Up until now I've been using a home-made Perl script to backup pictures from my cameras' SD cards to my PC, and then rsync'd to my storage servers. When I was away from home I couldn't make backups. The script was slow because it had to read EXIF metadata from every picture of the SD Card everytime I ran it.

This program provides two enhancements: The backup is done directly on a MinIO server thru HTTPS, and a SQLIte database is maintening an index of the pictures already processed, if no pictures are to be sent over the network the program ends very quickly.

My goal is to run this program on a autonomous Raspberry Pi with few hardware buttons and a small LCD or OLED screen to monitor the workflow. The Raspberry Pi could connect to the Internet from its Ethernet or WLAN ports, or even via a smartphone with USB tethering.
# Requirements
* ExifTool >= 8.40
* Python > 3.7
* PyExifTool https://github.com/smarnach/pyexiftool
* MinIO-py https://github.com/minio/minio-py
# Configuration
Copy `config.ini.sample` to whatever other file name and at least edit the MinIO section.

Edit `filetypes.json` to add the raw and video extensions used by your cameras.
# Usage
Mount a flash memory card or a Camera in storage mode (not MTP)

Run `python3 sync.py -c /path/to/the/config.ini -s /mountpoint/of/the/card`
# Warning
ALpha status, not suitable for production!
# Warning 2
This program is actually WRITING a small file at `/mountpoint/MISC/CONFERO/UUID.TXT` to track the card's pictures in the database. I didn't found another way to do this that is agnostic of camera models and filesystems :-(
# Todo
* Better code,
* Better documentation,
* Auto-backup of the SQLite database on the storage server,
* More command line options,
* Usage of object metadata and tags,
* so many more…
