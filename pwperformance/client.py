# https://github.com/AlekSi/codespeed-client
# MIT license
import json
import requests


class Client:
    required = ('benchmark', 'commitid', 'project', 'result_value')
    combined = required + ('branch', 'environment', 'executable', 'revision_date',
                           'result_date', 'min', 'max', 'std_dev')

    @classmethod
    def _update(cls, item, kwargs):
        for k, v in kwargs.items():
            if k not in cls.combined:
                raise KeyError("Unexpected key %r" % (k,))
            if v is not None:
                item[k] = v

    def __init__(self, root_url, environment, project, **kwargs):
        """ Kwargs passed here are defaults. """

        self.url = root_url + '/result/add/json/'
        self.data = []
        self.defaults = {
            'branch': 'default',
            'environment': environment,
            'project': project,
            'executable': 'Scipion'
        }
        self._update(self.defaults, kwargs)

    def add_result(self, **kwargs):
        """ kwargs passed here overwrite defaults. """

        item = self.defaults.copy()
        self._update(item, kwargs)

        missing = [k for k in self.required if k not in item]
        if missing:
            raise KeyError("Missing keys: %r" % missing)

        self.data.append(item)

    def upload_results(self):
        data, self.data = self.data, []
        r = requests.post(self.url,
                          data={"json": json.dumps(data)})

        #print("Sending data: ", data)
        return (r.status_code, r.text)
