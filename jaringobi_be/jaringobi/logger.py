import logging


def set_file_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app.log',  # Specify the file name for file-based logging (optional)
    )

    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)  # Set the desired logging level for the console handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Attach the console handler to the root logger
    logging.getLogger('').addHandler(file_handler)


# Configure the root logger
def setLogOptions():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app.log',  # Specify the file name for file-based logging (optional)
    )

    # Adding a console handler to display logs on the console as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the desired logging level for the console handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Attach the console handler to the root logger
    logging.getLogger('').addHandler(console_handler)