import os

class constants:
    def ROOT_PATH(self):
        return os.path.abspath(os.sep) #returns '/' on linux and C:\ on windows

    def TEMP_PATH(self):
        temp_path = os.path.join( self.ROOT_PATH(), 'DeliveryTracer' )

        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        return temp_path

    def PROJECT_PATH(self, project_name):
        temp_path = self.TEMP_PATH()
        project_path = os.path.join(temp_path, project_name)

        return project_path