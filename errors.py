class CustomTwitchError(Exception):
    """Custom Exception base class."""
    pass


class UserNotFoundError(CustomTwitchError):
    """Exception raised when twitch user not found."""
    pass


class UserChannelNotFoundError(CustomTwitchError):
    """Exception raised when twitch channel info not found."""
    pass


class UserCmdExistsError(CustomTwitchError):
    """Exception raised when user command already exists."""
    pass


class UserCmdDNEError(CustomTwitchError):
    """Exception raised when user command does not exist."""
    pass


