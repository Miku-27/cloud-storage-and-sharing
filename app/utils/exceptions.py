
class ServiceException(Exception):
    def __inti__(self,code,data=None):
        self.code = code 
        self.data = data

        super().__init__(code)