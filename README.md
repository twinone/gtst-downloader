# gtst-downloader
Simple python and bash scripts that given a video **token** does the following:
* Download the appropriate Apple HLS (.m3u8) file from rtlxl.nl
* Retrieve the playlist of the highest quality
* Download the 10 second .ts parts of the video (to /out/*.ts)
* Obtains the aes (128 bit) key to decrypt the .ts parts
* Decrypts all parts (to /out/*.dec.ts)
* Concatenates the parts into a single file and converts it to mp4

# Installation (Linux)
You'll need **python**, **libav-tools** and maybe some other packages I forgot
I use it on a digitalocean server, but you can also run it on your home Linux machine

# Usage
Get your **token** (explained below)
Download this project and run it:
```
git clone https://github.com/twinone/gtst-downloader.git
cd gtst-downloader
./download.py <your_token>
```

# Getting a video token
This currently only works for the soap serie Goede Tijden Slechte Tijden, but it should not be difficult to adapt to other videos from rtlxl.nl

1. Go to rtlxl.nl's [GTST section](http://rtlxl.nl/#!/gemist/goede-tijden-slechte-tijden-8926)
2. Click a video you want to see.
3. The last part of the url is your token

For example if you clicked the following video url:

http://rtlxl.nl/#!/goede-tijden-slechte-tijden-10821/c1cf06f1-84ac-305c-afce-7b948c98feef

Your token would be **c1cf06f1-84ac-305c-afce-7b948c98feef**
