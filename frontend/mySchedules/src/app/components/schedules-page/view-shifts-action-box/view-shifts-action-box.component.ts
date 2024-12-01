import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-view-shifts-action-box',
  templateUrl: './view-shifts-action-box.component.html',
  styleUrls: ['./view-shifts-action-box.component.css']
})
export class ViewShiftsActionBoxComponent implements OnInit {
  users: any[] = [];
  shiftRequests: any[] = [];
  status: any;
  shiftId: number | undefined;

  constructor(
    private http: HttpClient,
    public dialogRef: MatDialogRef<ViewShiftsActionBoxComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.shiftId = data.shiftId; // Get the shift ID passed via the dialog
    this.users = data.username;
    this.status = data.status;
  }

  ngOnInit(): void {
    // if (this.shiftId) {
    //   this.getEmployeesByShiftId(this.shiftId);
    // }
  }

  // getEmployeesByShiftId(shiftId: number): void {
  //   const apiUrl = `http://127.0.0.1:8000/users/getPickupRequests/`; // Example API endpoint
  //   const headers = { 'Content-Type': 'application/json' };
  //   const body = { shift_id: shiftId }; // Send the shift ID in JSON format

  //   this.http.post(apiUrl, body, { headers }).subscribe(
  //     (response: any) => {
  //       this.users = response.shift.employee.username || [];
  //     },
  //     error => {
  //       console.error('Error fetching shift requests:', error);
  //     }
  //   );
  // }

  approveUser(user: string): void {
    const apiUrl = `http://127.0.0.1:8000/users/approvePickupRequests/`; // Example API endpoint
    const headers = { 'Content-Type': 'application/json' };
    const body = { shift_id: this.shiftId, username: user }; // Send shift ID and username in JSON format
  
    this.http.post(apiUrl, body, { headers }).subscribe(
      response => {
        console.log(`User ${user} approved successfully`, response);
        // Optionally remove the approved user from the list
        // this.users = this.users.filter(u => u !== user);
        this.dialogRef.close();
      },
      error => {
        console.error('Error approving user:', error);
      }
    );
  }

  close(): void {
    this.dialogRef.close();
  }
}
