import os

class _Const:
    def ROOT_PATH(self):
        return os.path.abspath(os.sep) #returns '/' on linux and C:\ on windows

    def TEMP_PATH(self):
        return os.path.dirname( os.path.join( self.ROOT_PATH(), 'DeliveryTracer' ))

    def PROJECT_PATH(self, project_name):
        return os.path.dirname( os.path.join(self.TEMP_PATH(), project_name) )