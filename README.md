# Streaming Project App

Welcome to our streaming application project ! :notes:

## Usage

1. Put all the music files (in wav format) in the directory `/path/to/streaming-wav/streamapp/static/media/wav`
2. Generate the knwoledge database
```bash
$ python3 /path/to/streaming-wav/bddBuilder.py /path/to/streaming-wav/streamapp/static/media
```
3. Run the Web Server:
```bash
$ cd /path/to/streaming-wav
$ FLASK_APP=run.py FLASK_DEBUG=1 python -m flask run
```
4. Run the Streaming Server:
```bash
$ cd /path/to/streaming-wav/streamapp/static/media/
$ python3 /path/to/streaming-wav/streaming/RSTPServer.py
```
5. Run the Streaming Client:
```bash
$ python3 /path/to/streaming-wav/streaming/RTSPClient.py
```

## Team

* Nicola FOISSAC
* Loïc FAVRELIERE

At Université de La Rochelle - Digital Content Maganement module
