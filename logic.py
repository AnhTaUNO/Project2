from PyQt6.QtWidgets import *
from gui import *
import csv
import os


class Logic(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label_Text.setText("Please enter your ID and vote")
        self.label_Text.setStyleSheet("color:black")

        self.Button_submit.clicked.connect(self.submit_vote)

        #pull valid ID data
        self.id_list_file = "ID list.csv"
        self.valid_ids = set()
        if os.path.isfile(self.id_list_file):
            with open(self.id_list_file) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.valid_ids.add(row['ID'].strip())

        self.csv_file = "Vote results.csv"
        if not os.path.isfile(self.csv_file):
            with open(self.csv_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Candidate", "Vote"])

    def submit_vote(self):
        voter_id = self.Input_ID.text().strip()

        #format check
        if not (voter_id.isdigit() and len(voter_id) == 4):
            self.label_Text.setText("Enter a valid 4-digit ID Number!")
            self.label_Text.setStyleSheet("color:red")
            return

        #check valid data
        if voter_id not in self.valid_ids:
            self.label_Text.setText("ID not recognized!")
            self.label_Text.setStyleSheet("color:red")
            return

        #require/remind user to select button
        selected_button = self.buttonGroup.checkedButton()
        if not selected_button:
            self.label_Text.setText("Please select a candidate!")
            self.label_Text.setStyleSheet("color:red")
            return

        candidate = selected_button.text()

        with open(self.csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([candidate, 1])

        #Display results
        self.label_Text.setText("Vote submitted!")
        self.label_Text.setStyleSheet("color:green")

        #Reset inputs
        self.Input_ID.clear()
        self.buttonGroup.setExclusive(False)
        for button in self.buttonGroup.buttons():
            button.setChecked(False)
        self.buttonGroup.setExclusive(True)
