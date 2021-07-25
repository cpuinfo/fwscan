import logging
from fwscan.utils.console import console

log = logging.getLogger(__name__)


class ChecksecScanner(object):
    """Scanner for extracting, processing and visualizing
    protections in binary

    Examples usages:
    fwscan checksec --help
    fwscan checksec scan --help

    Scan folder /usr/bin and store results in folder output
    fwscan checksec scan /usr/bin output
    """

    def scan(self, folder, ofolder):
        """
        Scan for ELF binaries in the folder, extracts protection features
        and stores result in output file. Generates plots for each protection
        features.

        Args:
            folder (str): Target folder to scan
            ofolder (str): Output folder to store the results & plots
        """
        console.print("[bold green] :mag: Scanning")
        console.log("[bold green] Scanning")