#!/usr/bin/env python
import argparse
import logging
import sys
from importlib import reload
from typing import Mapping

from base.base_site import BaseSite
from sites.mintos import Mintos
from model import Site
from utils.file_impex import EXPORTS_FOLDER

PARSERS: Mapping[Site, BaseSite] = {
    Site.MINTOS: Mintos,
    Site.AUXMONEY: BaseSite,
    Site.BONDORA: BaseSite,
    Site.ESTATEGURU: BaseSite,
    Site.INVOYA: BaseSite,
    Site.LANDE: BaseSite,
    Site.MINTOS: BaseSite,
    Site.SWAPER: BaseSite,
    Site.TRINE: BaseSite,
    Site.VIAINVEST: BaseSite,
}


def main() -> None:
    args = __parse_args()
    __init_logging(args.log)
    sites: set[Site] = args.source
    for site in sites:
        p2p_site: BaseSite = PARSERS.get(site)
        logging.info(f"Parsing from {p2p_site}")
        p2p_site.login()
        p2p_site.get_statement(args)

        # navigate to statement download page
        # set filter (parse args)
        # download statement CSV or XLS
        # convert xls to csv (Bondora, ...)
        # reformat for pp -- can I use PP-P2P-Parser project here?


def __parse_args():
    argparser = argparse.ArgumentParser()
    all_available_sites = [source.value for source in Site]
    argparser.add_argument("-s", "--source", help="Source of the movie ratings", required=False, action="append", choices=all_available_sites)
    argparser.add_argument("-A", "--all-sources", help="Try to download from all available sources", action="store_true", default=False)
    argparser.add_argument("--earliest", help="earliest date of transactions to be considered", required=False)
    argparser.add_argument("--latest", help="latest date of transactions to be considered", required=False)
    argparser.add_argument("-d", "--destination", help="destination folder for result CSV file", required=False,
                           default=EXPORTS_FOLDER)
    argparser.add_argument("-x", "--show_browser", help="show the browser doing his work", action="store_true",
                           required=False)
    argparser.add_argument("--log", help="log level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], required=False)
    args = argparser.parse_args()
    if not args.source and not args.all_sources:
        raise ValueError("At least one source is required")
    args.source = {site for site in Site} if args.all_sources else set(Site(source) for source in args.source)
    return args


def __init_logging(log_level: str) -> None:
    log_level = getattr(logging, log_level.upper(), None)
    reload(logging)
    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


if __name__ == "__main__":
    main()
