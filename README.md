## Process Image

- Upload image example:
```bash
curl -F "image=@path/to/image" http://localhost:8000/process-image
```
- This will return a json response containing the `progress_url` and
`download_url`.
- `progress_url` can be used to check if image processing is done -- 0 indicate
that it's not started yet and 100 indicates done.
- Once progress is 100, `download_url` can be used to download the processed
image. Note that, it will return `404 Not Found` untill the processing of image
is done.

## Setup

- Clone or download the repository and change directory into it.
- Install the requirements:
```bash
python -m pip install -r requirements.txt
```
- Start the server by:
```bash
python manage.py runserver
```
- Run the image uploading intergration tests:
```bash
python manage.py test
```
- If all tests passed successfully, you're set up.

## Known Caveats

- Image processing gets executing on different thread, this ideally should be
implemented as message queue worker task e.g. celery tasks.
