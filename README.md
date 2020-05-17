# methinks

A vain attempt to make myself a bit more organized and supervisable.

* Create a **markdown** diary entry per day.
* Files support **TODO**s and general **note-taking** sections which track history across days.
* **Configure** your own sections using `config.yaml`
* If remote is installed, files can be synced across computers.

This is still work in progress: first week of trial and error started on *Sun 2020-04-26 21:53*.

## Installation

### Install with local support (persist only to files in local folder)

```bash
git clone https://github.com/andreasgrv/methinks
pip install --user -r requirements.txt
pip install --user .

# Add the following to your .bashrc (or any other way you want to source this)
export METHINKS_CONFIG="path/to/methinks/config/config.yaml"
```

You should now be ready to generate your first diary entry by running the `today` command.
```bash
today
```
To modify the structure of the entry, you can modify the [config](config/config.yaml) file.

### Install with remote support (persist to remote db)

#### Setup server
```bash
git clone https://github.com/andreasgrv/methinks
python3.7 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
pip install -e .

# You'll need to setup up a postgres database to match settings below
export METHINKS_DB_PORT="5432"
export METHINKS_DB_USER="methinks"
export METHINKS_DB_NAME="methinks"

export METHINKS_DB_PASSWD="mypass"
export METHINKS_TOKEN="My server token"

cd server
./run.sh
```

#### Update client to support sync with server

```bash
git clone https://github.com/andreasgrv/methinks
pip install --user -r requirements.txt
pip install --user .

# Add the following to your .bashrc (or any other way you want to source these)
export METHINKS_CONFIG="path/to/methinks/config/config.yaml"
export METHINKS_HOST="https://myserver-url"
export METHINKS_TOKEN="My server token"
```

## Todos

- [x] Add a blueprint to serve the files from a flask app
- [x] Make template configurable
- [ ] Make entries visible on my website
