from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from flask_wtf import Form


class ModelForm(Form):
    def __init__(self, *args, **kwargs):
        #self.model_class = kwargs.pop('model_class', None)
        self.instance = kwargs['obj'] = kwargs.pop('instance', None) or \
                                        kwargs.get('obj', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.instance:
            update = {}
            for name, field in self._fields.items():
                try:
                    if getattr(self.instance, name) != field.data:
                        update['set__' + name] = field.data
                except AttributeError:
                    raise Exception('Model %s has not attr %s but form %s has' \
                                    % (type(self.instance),
                                      name,
                                      type(self)))
            update['commit'] = commit
            self.instance.update(**update)
        else:
            self.instance = self.model_class(**self.data)
            if commit:
                self.instance.save()
        return self.instance
