import re
import yaml


class Pattern(object):
    def __init__(self, data_file):
        self.data_file = data_file
        self.load_yaml()
        self.setup_regexes()
        self.setup_patterns()

    def load_yaml(self):
        self.config = yaml.load(open(self.data_file))

    def setup_regexes(self):
        self.regexes = {}
        if self.config:
            for regex in self.config.get('regexes', []):
                if regex.get('compile', True):
                    self.regexes[regex.get('name')] = re.compile(r'{}'.format(
                        regex.get('regex')))
                else:
                    self.regexes[regex.get('name')] = r'{}'.format(
                        regex.get('regex'))

    def setup_patterns(self):
        self._patterns = self.config.get('patterns', {})
        if self._patterns:
            for key in self._patterns.keys():
                for p in self._patterns[key]:
                    if p['pattern'] in self.regexes:
                        p['pattern'] = self.regexes[p['pattern']]
                    if p['logstash'] in self.regexes:
                        p['logstash'] = self.regexes[p['logstash']]

    @property
    def patterns(self):
        return self._patterns
