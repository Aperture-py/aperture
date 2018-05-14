# Aperture

#### An image formatting and compression tool.


### Environment Setup
#### Note: See the following link for steps 1 and 2 if you're on Windows: https://docs.python.org/3/library/venv.html
1. Create a python virtual environment outside of the `aperture` directory: `python3 -m venv <my_env_name>`
2. Activate the virtual environment: `source <my_env_name>/bin/activate`
2. `cd` back into the `aperture` directory.
3. Install dependencies for the development environment: `pip install -r requirements.txt`


### Building aperture locally
1. Run: `make install`. This will install aperture as a python library and a source distribution in your virtual environment.


### TODO:
1. Define a styling format for yapf that we all agree on.
2. Define a documentation format that we all agree on (this is a good place to start: https://google.github.io/styleguide/pyguide.html)
3. If virtual environments start to become an issue for us while developing, we should switch to using pipenv to instead of using venv.
4. Figure out how to properly use docopt
5. Once we're past the goals for Week 2, we need to move the code for the CLI to a separate repository, where this `aperture` repo will only contain the stand-alone python library. 