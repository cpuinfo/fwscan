from scanfs.fsscanner import FileSystemScanner
import os
import subprocess
import logging
import subprocess
import errno
import shutil
import matplotlib.pyplot as plt
import pandas as pd

from fwscan.utils.console import console
from scanfs.fsscanner import FileSystemScanner


class CheckSecHelper(FileSystemScanner):
    def __init__(
        self,
        ifolder,
        ofolder: str,
        result_file="output.csv",
        fformat: str = "json",
        plot=False,
    ) -> None:
        super().__init__(ifolder)
        self.ifolder = ifolder
        self.ofolder = ofolder
        self.result_file = ofolder + "/" + result_file
        self.fformat = fformat
        self.plot = plot

        self.setup_output_folder()
        self.checksec_on_elfs()
        if plot:
            self.generate_plots()

    def checksec_dump(self, fpath, node):
        """
        Perform checksec and dump results in a file

        Args:
            result_fpath (str): Store results in this file path
            callback (function): Function called when the elf file type
            is found
        """
        try:
            path = os.path.join(fpath, node.name)
            completed_process = subprocess.run(
                ["checksec", "--format=" + str(self.fformat), "--file=" + str(path)],
                capture_output=True,
                check=True,
            )
            self.fd.write(completed_process.stdout.decode("utf-8"))
            self.fd.write("\n")
        except Exception as e:
            console.print("[red bold]An exception occurred: " + str(e))

    def checksec_on_elfs(self):
        """
        Checks the security features enabled on elf

        Args:
            filename (str): Filename to store the results of checksec in JSON
            fformat
        """
        self.fd = open(self.result_file, "w")
        self.fd.write(
            "RELRO,CANARY,NX,PIE,RPATH,RUNPATH,Symbols,FORTIFY,Fortified,Fortifiable,FILE"
        )
        self.fd.write("\n")
        self.scan_for_elfs(self.checksec_dump)
        self.fd.close()

    def generate_plots(self):
        plots_path = self.ofolder + "/plots"
        os.makedirs(plots_path, exist_ok=True)

        df = pd.read_csv(self.result_file)
        console.print("[bold red]Samples from the data frame")
        console.print(df.head(5))

        console.print("[bold green]Generating interesting plots for you!!!")
        for key in df.keys():
            console.print(key)
            figure = df[key].value_counts().plot(kind="bar").get_figure()
            figure.savefig(
                plots_path + "/" + key + ".svg", format="svg", dpi=600, pad_inches=0.5
            )

        os.chdir(self.ofolder)
        console.print("All plots generated in folder: " + plots_path)

    def setup_output_folder(self):
        try:
            os.mkdir(self.ofolder)
            console.print("[green]Created output folder: " + self.ofolder)
        except OSError as e:
            if e.errno == errno.EEXIST:
                console.print(
                    "[bold red]Output folder exists. Do you want to delete and recreate? (y/N): ",
                    justify="center",
                )
                choice = input()
                if choice == "Y" or choice == "y":
                    shutil.rmtree(self.ofolder, ignore_errors=True)
                    os.makedirs(self.ofolder, exist_ok=True)
                    console.print(
                        "[green]Created output folder: " + self.ofolder,
                        justify="center",
                    )
                    return True
                else:
                    console.print("[green]Keeping folder safe")
                    return False
        return True