
class Session:

    def __init__(self, session_id: str, data, is_new: bool):
        self.session_id = session_id
        self.data = data or {}
        self.is_new = is_new
        self.is_active = True
        self.modified = False

    def __getitem__(self, item: str, default: any = None):
        if self.__contains__(item):
            return self.data[item]
        return default

    def __setitem__(self, key, value):
        self.modified = True
        self.data[key] = value

    def __delitem__(self, key):
        self.modified = True
        del self.data[key]

    def __contains__(self, item: str):
        if item in self.data:
            return True
        return False

    def destroy(self):
        self.is_active = False