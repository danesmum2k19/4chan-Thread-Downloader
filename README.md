# 4chan-Thread-Downloader
Downloads files in specified 4chan threads (Non-interactive). Useful for scripts or general use.

Designed to run in Python 3 (May work in Python 2 [Not Recommended])

Requires wget and basc_py4chan

Install them with:

>sudo pip install basc_py4chan

>sudo pip install wget

Run
>./4download.py --help

for help

##Examples

Sample command to download all files from a thread:

>./4download.py --board [BOARD] --thread [THREAD ID] --all

Sample command to download GIFs and WebMs but not PNGs and JPGs:

>./4download.py --board [BOARD] --thread [THREAD ID] --gif --webm

Sample command to download PNGs and JPGs but not GIFs and WebMs:

>./4download.py --board [BOARD] --thread [THREAD ID] --png --jpg

Use flags in combinations to download only the files you want.

By default, the script creates a folder for the files. Use:

>--output [OUTPUT FOLDER]

to change that.

If I were to use the script on board wg and thread 234234, the created folder would be:

>wg_234234

Happy Downloading!
