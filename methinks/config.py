import os
import importlib
import yaml


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(MODULE_DIR)
DEFAULT_CONF_PATH = os.path.join(ROOT_DIR, 'config', 'config.yaml')


default_conf = None


class ConfigLoader(object):
    """Load and deal with methinks configuration"""

    EXPECTED_ROOT_FIELDS = ['sections']

    def __init__(self, conf, conf_filepath):
        super().__init__()
        self.conf = conf
        self.conf_filepath = conf_filepath

    def __repr__(self):
        entries = self.conf
        return yaml.dump(entries, sort_keys=False)

    def __getitem__(self, key):
        return self.conf[key]

    def __setitem__(self, key):
        # No reason to support mutability of config
        raise NotImplementedError

    @property
    def sections(self):
        return self.conf['sections']

    @property
    def triggers(self):
        triggers = dict()
        for sec in self.conf['sections']:
            module, classname = sec['handler'].rsplit('.', 1)
            module = importlib.import_module(module)
            cls = getattr(module, classname)
            triggers[sec['title']] = cls
        return triggers

    def export_env_variables(self):
        env_vars = dict()
        print('# From config at: %s' % self.conf_filepath)
        for env, sec in self.conf['env_variables'].items():
            parts = sec.split('.')[::-1]
            value = self.conf
            while parts:
                part = parts.pop()
                if value is not None:
                    value = value.get(part, None)
            if value is not None:
                env_vars[env] = value
        for k, v in env_vars.items():
            print("export %s='%s'" % (k, v))

    @classmethod
    def from_file(cl, filename):
        with open(filename, 'r') as f:
            opts = yaml.safe_load(f.read())
        assert(isinstance(opts, dict))
        assert(all(f in opts for f in cl.EXPECTED_ROOT_FIELDS))
        return cl(opts, conf_filepath=filename)


def get_default_conf():
    global default_conf
    if default_conf is None:
        default_conf = ConfigLoader.from_file(DEFAULT_CONF_PATH)
    return default_conf
