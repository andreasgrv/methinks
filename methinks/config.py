import importlib
import yaml


class ConfigLoader(object):
    """Load and deal with methinks configuration"""

    EXPECTED_ROOT_FIELDS = ['sections']

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def triggers(self):
        triggers = dict()
        for sec in self.sections:
            module, classname = sec['handler'].rsplit('.', 1)
            module = importlib.import_module(module)
            cls = getattr(module, classname)
            triggers[sec['title']] = cls
        return triggers

    @classmethod
    def from_file(cl, filename):
        with open(filename, 'r') as f:
            opts = yaml.safe_load(f.read())
        assert(isinstance(opts, dict))
        assert(all(f in opts for f in cl.EXPECTED_ROOT_FIELDS))
        return cl(**opts)
