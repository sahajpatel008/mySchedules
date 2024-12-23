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
  shiftstatus: any;
  shiftId: number | undefined;

  constructor(
    private http: HttpClient,
    public dialogRef: MatDialogRef<ViewShiftsActionBoxComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.shiftId = data.shift_id; // Get the shift ID passed via the dialog
    this.users = data.username;
    this.status = data.status;
  }

  ngOnInit(): void {
    if (this.status) {
      console.log(`User ${this.users} approved successfully`);
    }
    this.getEmployeesByShiftId(this.shiftId)
  }

  getEmployeesByShiftId(shiftId: any): void {
    console.log(this.shiftId)
    const apiUrl = `http://127.0.0.1:8000/users/getPickupRequests/`; // Example API endpoint
    const headers = { 'Content-Type': 'application/json' };
    const body = { shift_id: shiftId }; // Send the shift ID in JSON format

    this.http.post(apiUrl, body, { headers }).subscribe(
      (response: any) => {
        console.log(response);
        if (response.requests && response.requests.data) {
          // Map usernames into an array
          this.users = response.requests.data.map((item: any) => item.username);

          // Map shift_status into an array
          this.shiftstatus = response.requests.data[0].shift_status;
        } else {
          this.users = [];
          this.shiftstatus = null;
        }
        console.log(this.users,this.shiftstatus);
      },
      error => {
        console.error('Error fetching shift requests:', error);
      }
    );
  }

  approveUser(user: string): void {
    const apiUrl = `http://127.0.0.1:8000/users/approvePickupRequests/`; // Example API endpoint
    const headers = { 'Content-Type': 'application/json' };
    const body = { shift_request_id: this.shiftId, employee_id: user, username: localStorage.getItem('username')}; // Send shift ID and username in JSON format
  
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
