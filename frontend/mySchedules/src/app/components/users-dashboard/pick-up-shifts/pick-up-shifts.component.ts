import { HttpClient } from '@angular/common/http';
import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-pick-up-shifts',
  templateUrl: './pick-up-shifts.component.html',
  styleUrls: ['./pick-up-shifts.component.css']
})
export class PickUpShiftsComponent {
  params: any;
  shiftId: any;
  user: any;
  errorMessage: string = '';
  errorStatus: any;

  constructor(
    public dialogRef: MatDialogRef<PickUpShiftsComponent>,
    private http: HttpClient,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    console.log('modal data: ', data)
    this.shiftId = data.shift_id;
    this.user = data.username;
  }
  
  closeDialog() {
    this.dialogRef.close(this.params);
  }
  requestPickUp() {
    const apiUrl = `http://127.0.0.1:8000/users/pickupShift/`; // Example API endpoint
    const headers = { 'Content-Type': 'application/json' };
    const body = { username: this.user, shift_id: this.shiftId }; // Send the shift ID in JSON format
    console.log('body: ', body);

    this.http.post(apiUrl, body, { headers }).subscribe(
      (response: any) => {
        this.errorStatus = 0;
        console.log('Shift pickup request successful:', response);
        this.dialogRef.close('Success'); // Optionally close dialog with success message
      },
      error => {
        this.errorStatus = 1;
        console.error('Error fetching shift requests:', error);
        if (error.status === 400 && error.error.message === 'shift pickup request already exists.') {
          // Show error message if status 400 and specific message
          this.errorMessage = 'Shift pickup request already exists!';
         
        } else {
          this.errorMessage = 'An error occurred while processing your request. Please try again later.';
        }
      this.errorStatus = 0;
      }
    );
  }

}
