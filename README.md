# DPKG STATUS REST API

## Running the code

Steps to run the code:
```
# create and activate virtual environment, then run commands below
$ pip install -r ./requirements/prod.txt
$ pip install -r ./requirements/dev.txt

$ make run

# get list of all installed packages:
$ curl http://localhost:8000/ | jq .
[
  {
    "name": "adduser",
    "url": "/adduser"
  },
  {
    "name": "apt",
    "url": "/apt"
  },
  [cut]
]

# get details about a package
$ curl http://localhost:8000/libc6 | jq .
{
  "name": "libc6",
  "description": "GNU C Library: Shared libraries",
  "deps": [
    {
      "name": "libgcc-s1",
      "url": "/libgcc-s1"
    }
    [snip]
  ],
  "altdeps": [],
  "revdeps": [
    {
      "name": "apt",
      "url": "/apt"
    },
  [snip]
}

# run some tests (tests are horribly incomplete)
pytest
```


I didn't have time to finish tests.
