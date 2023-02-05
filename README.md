### Fetch-python

Downloads content from URLs given for offline storage and display ( to certain degree )

## Run in Docker

Build the image using docker in the source root ( image-name is your choice ): 

`docker build -t image-name .`

Start an interactive Docker shell using the image:

`docker run -ti image-name sh`

Use `fetch-py` executable to run the script:

`fetch-py https://www.google.com https://www.yahoo.com`


## Possible improvements

- Parse input URLs and check for validity
- Add more expansive offline resource filter
- Add local database for comparison of previous versions and offline resources