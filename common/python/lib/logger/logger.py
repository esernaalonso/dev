#######################################
# imports

#######################################
# functionality

def log_print(message, option="info", level=0):
    """Prints the log.

    Args:
        option (string, optional): Option to include a header in the log. "error", "warning", "info". By default "info"
        message (string): The message to print.
        level (int, optional): By default 0, includes extra level tabs in before the message.
    """

    message_to_print = message

    if option == "error":
        head_message = "# ERROR:   "
    elif option == "warning":
        head_message = "# WARNING: "
    elif option == "info":
        head_message = "# INFO:    "

    level_string = ""
    if level > 0:
        for i in range(level):
            level_string += "\t"

    message_to_print = message_to_print.replace("\n", ("\n# " + level_string))
    message_to_print = head_message + level_string + message_to_print

    print message_to_print


def info(message, level=0):
    """Prints the log.

    Args:
        message (string) The message to print.
        level (int, optional): By default 0, includes extra level tabs in before the message.
    """
    log_print(message, option="info", level=level)


def warning(message, level=0):
    """Prints the log.

    Args:
        message (string) The message to print.
        level (int, optional): By default 0, includes extra level tabs in before the message.
    """
    log_print(message, option="warning", level=level)


def error(message, level=0):
    """Prints the log.

    Args:
        message (string) The message to print.
        level (int, optional): By default 0, includes extra level tabs in before the message.
    """
    log_print(message, option="error", level=level)

#######################################
# execution

if __name__ == "__main__":
    # message = "This is a test\nyou know... hehehehehe."
    # info(message)
    # warning(message)
    # error(message)
    pass
