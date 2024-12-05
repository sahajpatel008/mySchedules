import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { ShiftCreatedModalComponent } from './shift-created-modal/shift-created-modal.component';

@Component({
  selector: 'app-shifts-action-box',
  templateUrl: './shifts-action-box.component.html',
  styleUrls: ['./shifts-action-box.component.css'],
})
export class ShiftsActionBoxComponent {
  selectedValue: any;
  selectedLocation: any;
  users: any;
  locations: any;
  data: any;
  date: any;
  times: string[] = [];
  start_time: string | null = null;
  end_time: string | null = null;
  selectedDate: Date | null = null;
  params: any;
  durationInSeconds = 5;
  
  constructor(
    public dialogRef: MatDialogRef<ShiftsActionBoxComponent>,
    private http: HttpClient,
    public dialog: MatDialog,
  ) {
    this.getLocations();
    this.generateTimeOptions();
  }

  getLocations(){
    const apiUrl = ' http://127.0.0.1:8000/users/getLocations/';
    const headers = { 'Content-Type': 'application/json' };

    this.params = {}

    this.http.post(apiUrl, this.params, { headers }).subscribe(
      (response: any) => {

        this.locations = response.locations;
      },
      error => console.error(error)
    );
  }

  ngOnInit(): void{
      //fetching data from json
      fetch('./assets/data.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok' + response.statusText);
        }
        return response.json();
      })
      .then(data => {
        this.users = data.users;
        // this.locations = data.location;
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });

  }

  onDateChange(event: any): void {
    this.date = event.value; 
  }

  generateTimeOptions(): void {
    const start = new Date();
    start.setHours(0, 0, 0, 0); // start time at midnight
    const end = new Date();
    end.setHours(23, 59, 59, 0); // end time at the end of the day

    const timeOptions: string[] = [];
    for (let time = start; time <= end; time.setMinutes(time.getMinutes() + 30)) {
      const formattedTime = time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      timeOptions.push(formattedTime);
    }

    this.times = timeOptions;
  }

  createShift(){
    const apiUrl = ' http://127.0.0.1:8000/users/makeShift/';
    const headers = { 'Content-Type': 'application/json' };

    this.params ={
      location: this.selectedLocation,
      date: this.date,
      start_time: this.start_time,
      end_time: this.end_time
    }

    this.http.post(apiUrl, this.params, { headers }).subscribe(
      response => console.log(response),
      error => console.error(error)
    );
    this.start_time = null;
    this.end_time = null;
    this.selectedDate = null;
    this.selectedLocation = null;
  }

  closeDialog() {
    this.dialogRef.close(this.params);
  }

  create_close_dialog(){
    this.createShift();
    const dialogRef = this.dialog.open(ShiftCreatedModalComponent, {
      panelClass: 'custom-modalbox',
      height: '10vh',
      width: '20vw'
    });

    setTimeout(() => {
      dialogRef.close();
    }, 2000);
  }
}
