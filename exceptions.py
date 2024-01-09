
class WrongPathException(Exception):
    'Raised when the path given does not exist'
    pass

class VideoReadError(Exception):
    'Raised when Opencv cannot read given video'
    pass