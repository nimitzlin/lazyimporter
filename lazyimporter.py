# -- coding: utf-8 -*-
__author__ = 'zbn4443'

import sys

class LazyFinder(object):
    def find_module(self, name, path):
        '''
        py2中，finder对象必须实现find_module()方法
        '''
        print "finder", name, path
        if not name.endswith("_data"):
                return None

        return LazyLoader(name, path)

class LazyLoader(object):
    def __init__(self, name, path):
        super(LazyLoader, self).__init__()
        self.name = name
        self.path = path

    def load_module(self, name):
        '''
        py2中，loader对象必须实现load_module()方法
        '''

        print "[LazyModule] init load", name
        return LazyModule(self.name, self.path)

class LazyModule(object):
    def __init__(self, name, path):
        super(LazyModule, self).__init__()
        self.name = name
        self.path = path
        self.module = None

    def __getattr__(self, attr):
        '''
        延迟加载模块，只有用到才加载
        '''
        if self.module is None:
            print '[LazyModule] try really load module:', self.name, ', path:', self.path
            if self.name in sys.modules:
                self.module = sys.modules[self.name]
                self.__dict__ = sys.modules[self.name].__dict__
                print '[LazyModule] module already import:', self.name, self.module
            else:
                hook = sys.meta_path.pop() if len(sys.meta_path) > 0 else None
                try:
                    self.module = __import__(self.name)
                    self.__dict__ = sys.modules[self.name].__dict__
                except Exception:
                    module_name = None
                    module = None
                    names = self.name.split( '.' )
                    for i in xrange(len(names)):
                        name = names[i]
                        if i == 1:
                            module_name = name
                        elif i > 1:
                            module_name += '.' + name
                        temp_module = self.get_module(module_name if module_name else name, module)
                        if temp_module is None:
                            module_name = name
                            temp_module = self.get_module(module_name if module_name else name, module)
                        module = temp_module
                    self.module = module
                    self.__dict__ = sys.modules[module_name].__dict__

                if hook:
                    sys.meta_path.append(hook)

        return self.__dict__[attr]

    def get_module( self, name, parent ):
        parent_name = getattr( parent, '__name__', '' )
        parent_path = getattr( parent, '__path__', None)
        if parent_name:
            full_name = parent_name + '.' + name
        else:
            full_name = name

        module = sys.modules.get(full_name)
        if module:
            return module

        return self.create_module( name, full_name, parent_path )

    def create_module( self, name, full_name, parent_path ):
        try:
            module = __import__(name)
        except Exception, e:
            print '[LazyModule] import error! name:%s, full_name:%s, parent_path:%s, e:%s' % (name, full_name, parent_path, e)
            return None
        else:
            return module

sys.meta_path.append(LazyFinder())
