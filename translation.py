from factory import Factory
import os
import configparser

Config = Factory.get('Config')

class Translation(object):
    def __init__(self):
        """
        Load language file as well as default file
        """

        self.parser_default = self._load('english')
        self.parser = self._load(Config.language_file)

        print(self.get('language_loaded'))

    def _load(self,language_file):
        """
        Load language file
        """
        path = os.path.dirname(os.path.realpath(__file__))
        full_file_name = '{}/ark/lang/{}.ini'.format(path,language_file)

        if not os.path.isfile(full_file_name):
            raise Exception('Unable to find language file: ', full_file_name)

        try:
            parser = configparser.ConfigParser()
            parser.read(full_file_name)
        except Exception as e:
            print('Failed to load language file: ', language_file)
            raise

        return parser

    def get(self,key,section='Generic'):
        """ Get a translation for variable: key

        Args:
            key: Required. Key in translation file
            section: Optional. Section to find key. Default to "generic"
        """
        result = None
        try:
            result = self.parser.get(section,key)
        except configparser.NoSectionError as e:
            result = 'LANGUAGE FAILURE! UNSPECIFIED SECTION'
            print('LANGUAGE ERROR: Unable to find language section: ', section)
        except configparser.NoOptionError as e:
            result = 'LANGUAGE FAILURE! UNSPECIFIED KEY'
            print('LANGUAGE ERROR: Unable to find language key "{}" in section "{}"'.format(key,section))

        return result