#!/bin/python
import logging.config

if __name__ == "__main__":
    logging.config.fileConfig("logging.ini")
    logger = logging.getLogger("test")
    logger.info("test...")
