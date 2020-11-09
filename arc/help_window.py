#  This software was developed by United States Army Corps of Engineers (USACE)
#  employees in the course of their official duties.  USACE used copyrighted,
#  open source code to develop this software, as such this software 
#  (per 17 USC § 101) is considered "joint work."  Pursuant to 17 USC § 105,
#  portions of the software developed by USACE employees in the course of their
#  official duties are not subject to copyright protection and are in the public
#  domain.
#  
#  USACE assumes no responsibility whatsoever for the use of this software by
#  other parties, and makes no guarantees, expressed or implied, about its
#  quality, reliability, or any other characteristic. 
#  
#  The software is provided "as is," without warranty of any kind, express or
#  implied, including but not limited to the warranties of merchantability,
#  fitness for a particular purpose, and noninfringement.  In no event shall the
#  authors or U.S. Government be liable for any claim, damages or other
#  liability, whether in an action of contract, tort or otherwise, arising from,
#  out of or in connection with the software or the use or other dealings in the
#  software.
#  
#  Public domain portions of this software can be redistributed and/or modified
#  freely, provided that any derivative works bear some notice that they are
#  derived from it, and any modified versions bear some notice that they have
#  been modified. 
#  
#  Copyrighted portions of the software are annotated within the source code.
#  Open Source Licenses, included in the source code, apply to the applicable
#  copyrighted portions.  Copyrighted portions of the software are not in the
#  public domain.

######################################
##  ------------------------------- ##
##          help_window.py          ##
##  ------------------------------- ##
##      Writen by: Jason Deters     ##
##  ------------------------------- ##
##    Last Edited on: 2020-06-22    ##
##  ------------------------------- ##
######################################

import os
import sys
import tkinter
from tkinter import ttk
import time

import subprocess
import webbrowser

# Custom Libraries
try:
    from . import get_all
    from . import get_files
    from .utilities import JLog
except Exception:
    #  Maintains compatibility with previous non-compiled versions
    import get_all
    import get_files
    # Reverse compatibility step - Add utilities folder to path directly
    MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
    ROOT = os.path.dirname(MODULE_PATH)
    PYTHON_SCRIPTS_FOLDER = os.path.join(ROOT, 'Python Scripts')
    TEST = os.path.exists(PYTHON_SCRIPTS_FOLDER)
    if TEST:
        UTILITIES_FOLDER = os.path.join(PYTHON_SCRIPTS_FOLDER, 'utilities')
        sys.path.append(UTILITIES_FOLDER)
    else:
        ARC_FOLDER = os.path.join(ROOT, 'arc')
        UTILITIES_FOLDER = os.path.join(ARC_FOLDER, 'utilities')
        sys.path.append(UTILITIES_FOLDER)
    import JLog



ABOUT_HELP_TEXT = """This tool was created to facilitate the comparison of the precipitation at a given location and date to the normal
precipitation range at that location over the preceding 30 years. Under the final Navigable Waters Protection Rule
(NWPR), determining the jurisdictional status of a waterbody is generally informed by understanding conditions in a
“typicalyear” – i.e., the normal periodic range of precipitation and other climate variables for that waterbody. This
tool is not necessary to implement the Navigable Waters Protection Rule or the concept of “typical year” in that rule.
Updates to this tool may be made over time, and will be indicated by a change in the version number and date in the
on-screen display and in the documentation generated by the tool.

For questions regarding the day-to-day use of the APT or NWPR Policy or Implementation, contact the USEPA
at:  CWAwotus@EPA.GOV

To report errors with this program, click the "Report Issue" button or email:  APT-Report-Issue@usace.army.mil"""



class Main(object):
    """GUI for the Help Page of the Antecedent Precipitation Tool"""

    def __init__(self):
        self.log = JLog.PrintLog()
        self.ula_ccepted = False
        self.button_labels = []
        self.pdf_buttons = []
        self.youtube_buttons = []
        self.separators = []
        self.num_usage_single = 0
        self.num_usage_watershed = 0
        self.row = 0
        # Find Root Folder
        module_path = os.path.dirname(os.path.realpath(__file__))
        root_folder = os.path.split(module_path)[0]

        # Create Master Frame
        self.master = tkinter.Tk()
        #width = 978
        #height = 735
        #self.master.geometry("{}x{}+431+332".format(width, height))
        self.master.geometry("")
        #self.master.minsize(width, height)
        #self.master.maxsize(1370, 749)
        self.master.resizable(1, 1)
        self.master.title("About the Antecedent Precipitation Tool")

        # Set Window Icon
        try:
            images_folder = os.path.join(root_folder, 'images')
            graph_icon_file = os.path.join(images_folder, 'Graph.ico')
            self.master.wm_iconbitmap(graph_icon_file)
        except Exception:
            images_folder = os.path.join(sys.prefix, 'images')
            graph_icon_file = os.path.join(images_folder, 'Graph.ico')
            self.master.wm_iconbitmap(graph_icon_file)
        
        # Create an additional level of frame just so everything stays together when the window is maximized
        self.primary_frame = ttk.Frame(self.master)
        self.primary_frame.grid()


        #---GENERAL INFORMATION TEXT BOX---#

        # Create separate frame for Textbox and Scrollbar
        self.text_frame = ttk.Frame(self.primary_frame)
        self.text_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=0)
    
        # Create General Info
        self.label_general_top=ttk.Label(self.text_frame,
                                         text="General Information",
                                         font='Helvetica 11 bold')
        self.label_general_top.grid(row=0, column=0, padx=0, pady=0)

        # Create configure, and Grid Text Box
        self.general_text = tkinter.Text(self.text_frame, height=12, width=119) # creating a textbox for getting address
        self.scrollbar = tkinter.ttk.Scrollbar(self.text_frame)  # making a scrolbar with entry test text field
        self.general_text.config(yscrollcommand=self.scrollbar.set)  # setting scrolbar to y-axis
        self.scrollbar.config(command=self.general_text.yview)  # setting the scrolbar to entry test textbox        
        self.general_text.insert('end', ABOUT_HELP_TEXT) # Inserting the About/Help Text 
        self.general_text.config(state='disabled')
        self.general_text.grid(column=0, row=1, sticky='nsew') # set entry to Specific column of bottom frame grid
        self.scrollbar.grid(column=1, row=1, sticky='nsw') # set self.scrollbar to Specific column of bottom frame grid

        # Create FRAME for Central Buttons
        self.central_buttons_frame = ttk.Frame(self.primary_frame)
        self.central_buttons_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=0)
        self.add_separator(self.central_buttons_frame)
        # Create/Grid LABEL for SINGLE POINT USAGE
        self.label_usage_single = ttk.Label(self.central_buttons_frame,
                                            text="Calculating the Antecedent Rainfall Condition at a single point",
                                            font='Helvetica 11 bold')
        self.label_usage_single.grid(row=self.row, column=0, padx=0, pady=0, sticky="w", columnspan=1)
        self.row += 1
        # Create/Grid ITEMS for SINGLE POINT USAGE
        docs_folder = os.path.join(root_folder, 'help')
        self.add_reference(frame='Usage-Single',
                           title='How to read the output of a single-point analysis:',
                           pdf_local_path=os.path.join(docs_folder, 'APT - How to Read the Output of a Single-Point Analysis.pdf'),
                           pdf_url=r"https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT - How to Read the Output of a Single-Point Analysis.pdf",
                           youtube_url=None)
        self.add_reference(frame='Usage-Single',
                           title='How to generate a single-point analysis for a given date:',
                           pdf_local_path=os.path.join(docs_folder, 'APT Walkthrough - Single Point - Single Date.pdf'),
                           pdf_url=r"https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT Walkthrough - Single Point - Single Date.pdf",
                           youtube_url=None)
        self.add_reference(frame='Usage-Single',
                           title='How to generate a single-point analysis for several dates at once:',
                           pdf_local_path=os.path.join(docs_folder, "APT Walkthrough - Single Point - Multiple Dates.pdf"),
                           pdf_url=r"https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT Walkthrough - Single Point - Multiple Dates.pdf",
                           youtube_url=None)
        self.add_reference(frame='Usage-Single',
                           title='How to generate a single-point analysis for many dates using a spreadsheet:',
                           pdf_local_path=os.path.join(docs_folder, "APT Walkthrough - Single Point - Many Dates Using CSV Input.pdf"),
                           pdf_url=r"https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT Walkthrough - Single Point - Many Dates Using CSV Input.pdf",
                           youtube_url=None)
        self.add_reference(frame='Usage-Single',
                           title='How to generate a single-point analysis at a daily frequency for a given date range:',
                           pdf_local_path=os.path.join(docs_folder, "APT Walkthrough - Single Point - Daily Frequency Date Range.pdf"),
                           pdf_url=r"https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT Walkthrough - Single Point - Daily Frequency Date Range.pdf",
                           youtube_url=None)
        self.add_separator(self.central_buttons_frame)


        #---WATERSHED SCALE USAGE---#

        # Create/Grid LABEL for WATERSHED SCALE USAGE
        self.label_methodology=ttk.Label(self.central_buttons_frame,
                                             text="Aggregating the Antecedent Rainfall Condition of Random Sampling Points within a Watershed",
                                             font='Helvetica 11 bold')
        self.label_methodology.grid(row=self.row, column=0, padx=0, pady=0, sticky="w", columnspan=1)
        self.row += 1
        # Create/Grid ITEMS for WATERSHED SCALE USAGE
        self.add_reference(frame='Usage-Watershed',
                           title='How to read the output of a Watershed analysis:',
                           pdf_local_path=os.path.join(docs_folder, 'APT - How to Read the Output of a Watershed Analysis.pdf'),
                           pdf_url=r"https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT - How to Read the Output of a Watershed Analysis.pdf",
                           youtube_url=None)
        self.add_reference(frame='Usage-Watershed',
                           title='How to generate a watershed analysis using the USGS Watershed Boundary Dataset:',
                           pdf_local_path=os.path.join(docs_folder, 'APT Walkthrough - Watershed - WBD.pdf'),
                           pdf_url="https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT Walkthrough - Watershed - WBD.pdf",
                           youtube_url=None)
        self.add_reference(frame='Usage-Watershed',
                           title='How to generate a watershed analysis using a custom Watershed Polygon:',
                           pdf_local_path=os.path.join(docs_folder, 'APT Walkthrough - Watershed - Custom.pdf'),
                           pdf_url="https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT Walkthrough - Watershed - Custom.pdf",
                           youtube_url=None)
        self.add_separator(self.central_buttons_frame)

        #---METHODOLOGY---#

        # Create/Grid LABEL for WATERSHED SCALE USAGE
        self.label_methodology=ttk.Label(self.central_buttons_frame,
                                         text="Methodology References",
                                         font='Helvetica 11 bold')
        self.label_methodology.grid(row=self.row, column=0, padx=0, pady=0, sticky="w", columnspan=1)
        self.row += 1
        # Create/Grid ITEMS for WATERSHED SCALE USAGE
        self.add_reference(frame='Methodology',
                           title='User Guide (Narrative Format):',
                           pdf_local_path=os.path.join(docs_folder, 'APT - User Guide.pdf'),
                           pdf_url="https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT - User Guide.pdf",
                           youtube_url=None)
        self.add_reference(frame='Methodology',
                           title="Detailed Methodology - Step-by-step Description the Entire Process:",
                           pdf_local_path=os.path.join(docs_folder, 'APT - Detailed Methodology.pdf'),
                           pdf_url="https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/APT - Detailed Methodology.pdf",
                           youtube_url=None)
        self.add_reference(frame='Methodology',
                           title='Accessing and Using Meteorological Data to Evaluate Wetland Hydrology (Sprecher and Warne, 2000):',
                           pdf_local_path=os.path.join(docs_folder, 'Sprecher and Warne.pdf'),
                           pdf_url="https://github.com/jDeters-USACE/Antecedent-Precipitation-Tool/raw/master/help/Sprecher and Warne.pdf",
                           youtube_url=None)
        self.add_separator(self.central_buttons_frame)


        #---BOTTOM BUTTONS---#

        # Create/Grid Close Button
        self.button_close = ttk.Button(self.primary_frame,
                                       text="Close This Window",
                                       command=self.click_close_button)
        self.button_close.grid(row=self.row, column=0, pady=12, padx=100, sticky='w')

        # Create/Grid Close Button
        self.button_close = ttk.Button(self.primary_frame,
                                       text="Report Issue",
                                       command=self.click_report_issue_button)
        self.button_close.grid(row=self.row, column=0, pady=12, padx=200, sticky='e')


        # Configure rows/columns
        self.master.geometry("+800+400")
        # Configure rows and columns
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        # a trick to activate the window (on windows 7)
        self.master.deiconify()
        # End of __init__ method


    def add_separator(self, frame):
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=self.row, sticky='ew', columnspan=3, pady=3)
        self.row += 1
        self.separators.append(separator)


    def add_reference(self, frame, title, pdf_local_path=None, pdf_url=None, youtube_url=None):
        # Create/Grid LABEL
        label = ttk.Label(self.central_buttons_frame,
                              text=title,
                              font='Helvetica 10 bold')
        label.grid(row=self.row, column=0, padx=25, pady=5, sticky='w')
        self.button_labels.append(label)
        # Create/Grid PDF BUTTON
        if pdf_local_path is not None:
            def open_pdf_reference():
                local_file_name = os.path.split(pdf_local_path)[1]
                local_file_name_no_ext = os.path.splitext(local_file_name)[0]
                module_path = os.path.dirname(os.path.realpath(__file__))
                root = os.path.dirname(module_path)
                version_folder = os.path.join(root, 'v')
                version_local_path = os.path.join(version_folder, local_file_name_no_ext)
                version_url = 'https://raw.githubusercontent.com/jDeters-USACE/Antecedent-Precipitation-Tool/master/v/{}'.format(local_file_name_no_ext)
                get_files.get_only_newer_version(file_url=pdf_url,
                                                 local_file_path=pdf_local_path,
                                                 version_url=version_url,
                                                 version_local_path=version_local_path)
                pdf_name = os.path.split(pdf_local_path)[1]
                print('Opening {}...'.format(pdf_name))
                time.sleep(2)
                subprocess.Popen(pdf_local_path, shell=True)
                print('')
                print('Ready for new input.')
            if pdf_local_path == '':
                pdf_text = "PDF Instructions (Coming Soon!)"
            else:
                pdf_text = 'PDF Instructions'
            pdf_button = ttk.Button(self.central_buttons_frame,
                                    text=pdf_text,
                                    command=open_pdf_reference)
            pdf_button.grid(row=self.row, column=1, padx=10, pady=5, sticky='e')
            # Auto-disable before link provided
            if pdf_local_path == '':
                pdf_button.config(state='disabled')
            self.pdf_buttons.append(pdf_button)
        # Create/Grid YOUTUBE BUTTON
        if youtube_url is not None:
            # Create function that opens URL in default browser
            def open_youtube_url():
                webbrowser.open(youtube_url, new=1, autoraise=True)
            # Asign function to new button
            if youtube_url == '':
                youtube_text = "YouTube Demo (Coming Soon!)"
            else:
                youtube_text = 'YouTube Demonstration'
            youtube_button = ttk.Button(self.central_buttons_frame,
                                        text=youtube_text,
                                        command=open_youtube_url)
            youtube_button.grid(row=self.row, column=2, padx=0, pady=5, sticky='e')
            # Auto-disable before link provided
            if youtube_url == '':
                youtube_button.config(state='disabled')
            self.youtube_buttons.append(youtube_button)
        self.row += 1
    # End of add_reference Method



    def click_report_issue_button(self):
        """
        If Outlook present:
        Drafts and email with the current error log as an attachment directed to me

        If Outlook not present:
        Opens the Error Log and requests that users transmit it with their error report.
        """
        self.log.send_log()
    # End of send_log method

    def click_close_button(self):
        self.ula_ccepted = True
        self.master.destroy() # Close ULA window
        return False

    def run(self):
        self.master.mainloop()

def click_how_to_run_point_button():
    # Define File Path
    # Ensure Exists
    # Popen PDF
    # Announce ready for new input
    print('')
    print('Ready for new input.')
    return



def open_youtube_link(youtube_url):
    # Define File Path
    # Ensure Exists
    # Popen PDF
    # Announce ready for new input
    print('')
    print('Ready for new input.')
    return

if __name__ == '__main__':
    APP = Main()
    APP.run()
