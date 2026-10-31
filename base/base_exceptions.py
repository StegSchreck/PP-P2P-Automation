class ParserException(Exception):
    pass


class LoginFailedException(ParserException):
    pass


class CaptchaPresentException(LoginFailedException):
    pass


class CSVDownloadFailedException(ParserException):
    pass


class NoValidCredentialsException(ParserException):
    pass


class SiteNotReachableException(ParserException):
    pass
