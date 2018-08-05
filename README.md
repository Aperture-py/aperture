# Aperture

#### An image formatting and compression tool.


### Environment Setup
We'll be using `pipenv` to manage our virtual environment, and dev dependencies for the project.
1. Install pipenv: `pip install pipenv`.
2. `cd` into `aperture` and initialize the virtual environment: `pipenv install`. 
3. Enable the virtual environment: `pipenv shell`.
4. You're good to go! Refer to the `pipenv` docs for installing dependencies and much more: https://docs.pipenv.org/


### Building aperture locally
1. Install aperture as a python library and a source distribution in your virtual environment: `make install`.
2. Remove left over build artifacts: `make clean`.

### TODO:
1. Register aperture to the PyPi index (aperture already taken, so `aperturepy` will probably suffice).
2. Define a styling format for yapf that we all agree on.
3. Define a documentation format that we all agree on (this is a good place to start: https://google.github.io/styleguide/pyguide.html).
4. Figure out how to properly use docopt.
5. Once we're past the goals for Week 2 (basic CLI functionality), we need to move the code for the CLI to a separate repository, where this `aperture` repo will only contain the stand-alone python library. 