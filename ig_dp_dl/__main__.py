#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main module of the ig_dp_dl package.

This module contains the main function of the package.

Functions:
    main() -> int: Main function.
"""
from rich.traceback import install

from .cli import exit_session, get_parsed_args
from .consts import DEBUG, EXIT_SUCCESS, PROFILE
from .scrapper import send_request
from .logs import logger


def main() -> int:
    """
    Main function
    """
    args = get_parsed_args()

    logger.info("Start of session")

    username = ""
    send_request(username)

    exit_session(EXIT_SUCCESS)


if __name__ == "__main__":
    # Enable rich error formatting in debug mode
    install(show_locals=DEBUG)
    if DEBUG:
        print("[yellow]Debug mode is enabled[/yellow]")
    if PROFILE:
        import cProfile

        print("[yellow]Profiling is enabled[/yellow]")
        cProfile.run("main()")
    else:
        main()
