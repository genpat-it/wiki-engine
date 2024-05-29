# GENPAT Wiki Engine

Mkdocs based engine to produce wiki and PDF documents from a set of markdown files.

## docker 

Go to the directory with `mkdocs.yml` file (see `examples` dir). Then

```sh
# basic launch with serve at 8001 port
docker run --env HOME=/home/$USER -it -u `id -u`:`id -g` -p 8001:8000 --rm -v $(pwd):/home/$USER -w /home/$USER ghcr.io/genpat-it/wiki-engine:main sh -c 'mkdocs serve --watch-theme -f mkdocs.yml -a 0.0.0.0:8000 '

# launch with watch-theme option
docker run --env HOME=/home/$USER -it -u `id -u`:`id -g` -p 8001:8000 --rm -v $(pwd):/home/$USER -w /home/$USER ghcr.io/genpat-it/wiki-engine:main sh -c 'mkdocs serve --watch-theme -f mkdocs.yml -a 0.0.0.0:8000 '
```
