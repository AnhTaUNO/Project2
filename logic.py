from PyQt6.QtWidgets import *
from gui import *
import csv
import os


class VotingApp(QDialog, Ui_Dialog):
    """Dialog window for casting and recording votes."""

    def __init__(self) -> None:
        """
        Initialize the voting dialog:
            connects the submit button.
            loads valid voter IDs,
            ensures the results file exists,
            creates a csv file and its first row
        """

        super().__init__()
        self.setupUi(self)

        # Initialize UI text
        self.label_Text.setText("Please enter your ID and vote")
        self.label_Text.setStyleSheet("color:black")

        # Connect submit button
        self.Button_submit.clicked.connect(self.submit_vote)

        #pull valid ID data
        self.id_list_file = "ID list.csv"
        self.valid_ids = set()
        try:
            if os.path.isfile(self.id_list_file):
                with open(self.id_list_file) as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        self.valid_ids.add(row.get('ID').strip())
        except (FileNotFoundError, PermissionError):
            self.label_Text.setText("ID list file not found or inaccessible")
            self.label_Text.setStyleSheet("color:red")
        except csv.Error:
            self.label_Text.setText("Malformed CSV in ID list")
            self.label_Text.setStyleSheet("color:red")
        except KeyError:
            self.label_Text.setText("ID column missing in CSV")
            self.label_Text.setStyleSheet("color:red")

        #create Vote results csv file if not available in the folder
        self.csv_file = "Vote results.csv"
        try:
            if not os.path.isfile(self.csv_file):
                with open(self.csv_file, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Voter ID","Candidate"])
        except Exception:
            self.label_Text.setText("Error initializing results file.")
            self.label_Text.setStyleSheet("color:red")

        #load already voted IDs
        self.voted_ids = set()
        if os.path.isfile(self.csv_file):
            with open(self.csv_file) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.voted_ids.add(row.get('Voter ID').strip())

    def submit_vote(self) -> None:
        """
        Validate the entered voter ID and selected candidate,
        prevent duplicate votes
        append to CSV, and update the UI status label.

        """

        voter_id = self.Input_ID.text().strip()

        #format check
        if not (voter_id.isdigit() and len(voter_id) == 4):
            self.label_Text.setText("Enter a valid 4-digit ID Number!")
            self.label_Text.setStyleSheet("color:red")
            return

        #duplicate vote check
        if voter_id in self.voted_ids:
            self.label_Text.setText("Already voted!")
            self.label_Text.setStyleSheet("color:red")
            return

        #valid data check
        if voter_id not in self.valid_ids:
            self.label_Text.setText("ID not recognized!")
            self.label_Text.setStyleSheet("color:red")
            return

        #require/remind user to select candidate
        selected_button = self.buttonGroup.checkedButton()
        if not selected_button:
            self.label_Text.setText("Please select a candidate!")
            self.label_Text.setStyleSheet("color:red")
            return

        candidate = selected_button.text()

        #append vote data from user to Vote results csv file
        try:
            with open(self.csv_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([voter_id,candidate])
            #mark as voted
            self.voted_ids.add(voter_id)
        except Exception:
            self.label_Text.setText("Error submitting vote.")
            self.label_Text.setStyleSheet("color:red")
            return

        #Display successful results
        self.label_Text.setText("Vote submitted!")
        self.label_Text.setStyleSheet("color:green")

        #Reset inputs
        self.Input_ID.clear()
        self.buttonGroup.setExclusive(False)
        for button in self.buttonGroup.buttons():
            button.setChecked(False)
        self.buttonGroup.setExclusive(True)
