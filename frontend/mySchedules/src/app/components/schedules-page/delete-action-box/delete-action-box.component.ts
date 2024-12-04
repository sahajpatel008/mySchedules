import { HttpClient } from '@angular/common/http';
import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-delete-action-box',
  templateUrl: './delete-action-box.component.html',
  styleUrls: ['./delete-action-box.component.css']
})
export class DeleteActionBoxComponent {
  shiftId: number | undefined;
  isDialogOpen: boolean = false;
  constructor(
    private http: HttpClient,
    public dialogRef: MatDialogRef<DeleteActionBoxComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.shiftId = data.shift_id; // Get the shift ID passed via the dialog
  }
  

  openDeleteDialog() {
    this.isDialogOpen = true; // Open the delete dialog
  }

  closeDialog() {
    this.dialogRef.close();
    this.isDialogOpen = false; // Close the dialog without deleting
  }

  deleteShift(){
    const apiUrl = `http://127.0.0.1:8000/users/deleteShifts/`; // Example API endpoint
    const headers = { 'Content-Type': 'application/json' };
    const body = { shift_id: this.shiftId }; // Send the shift ID in JSON format

    this.http.post(apiUrl, body, { headers }).subscribe(
      (response: any) => {
        console.log("Opened delete shift dialog");
        this.dialogRef.close();
      },
      error => {
        console.error('Error fetching shift requests:', error);
      }
    );
  }
}
