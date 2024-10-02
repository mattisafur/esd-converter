import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox

import dism_operations


class EsdConverter(tk.Frame):
    def __init__(self, master) -> None:
        self.master = master
        tk.Frame.__init__(self, self.master)

        # .esd selection path entry and button
        self.esd_file_path_entry = tk.Entry(self.master)
        self.esd_file_path_entry.pack()
        self.esd_file_selection_button = tk.Button(
            self.master, text="Browse", command=self.browse_esd_file
        )
        self.esd_file_selection_button.pack()

        # convert button
        self.convert_button = tk.Button(
            self.master, text="Covert", command=self.convert_to_wim
        )
        self.convert_button.pack()

    def browse_esd_file(self) -> None:
        # open file dialog and set path in entry to the selected file
        file_types = [("ESD files", "*.esd"), ("All files", "*.*")]

        file_path: str = fd.askopenfilename(title="Select file", filetypes=file_types)

        self.esd_file_path_entry.insert(0, file_path)

    def convert_to_wim(self) -> None:
        # prompt to select the file location and name to export the images to
        file_types = [("WIM file", "*.wim")]

        # get source path from entry
        source_path: str = self.esd_file_path_entry.get()
        if source_path == "":
            messagebox.showerror(
                title="Error", message="Please enter the path to the ESD file."
            )
            raise FileNotFoundError

        destination_path: str = fd.asksaveasfilename(
            title="Export as", initialfile="install.wim", filetypes=file_types
        )

        # get and parse images from dism
        try:
            dism_output: str = dism_operations.dism_get_wiminfo(source_path)
        except FileNotFoundError:
            self.raise_file_not_found_error()
            raise FileNotFoundError
        images: list[dict[str, str]] = dism_operations.parse_dism_get_wiminfo_output(
            dism_output
        )

        for image in images:
            try:
                dism_operations.dism_export_image(
                    source_path, image["Index"], destination_path
                )
            except FileNotFoundError:
                self.raise_file_not_found_error()
                raise FileNotFoundError

    def raise_file_not_found_error(self) -> None:
        messagebox.showerror(
            title="Error",
            message="The file entered does not exist.",
        )


if __name__ == "__main__":
    root = tk.Tk()
    EsdConverter(root)
    root.mainloop()
