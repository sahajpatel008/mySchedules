import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-shifts-action-box',
  templateUrl: './shifts-action-box.component.html',
  styleUrls: ['./shifts-action-box.component.css']
})
export class ShiftsActionBoxComponent {
  selectedValue: any;
  selectedLocation: any;
  users: any;
  locations: any;
  data: any;
  date: any;
  times: string[] = [];
  start_time: string = '';
  end_time: string = '';
  params: any;

  constructor(
    public dialogRef: MatDialogRef<ShiftsActionBoxComponent>,
    private http: HttpClient
  ) {
    this.generateTimeOptions();
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
              this.locations = data.location;
            })
            .catch(error => {
              console.error('There was a problem with the fetch operation:', error);
            });

            //call api function
            // this.getData();
  }

  onDateChange(event: any): void {
    this.date = event.value; // This is the selected date
    console.log('Selected Date:', this.date);
  }

  getData(): void {
    const apiUrl = '';
    this.http.get(apiUrl).subscribe(
      (response) => {
        this.data = response; // Handle the response here
        console.log(this.data);
      },
      (error) => {
        console.error('API call failed:', error); // Handle errors
      }
    );
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
  }

  closeDialog() {
    this.dialogRef.close(this.params);
  }
  create_close_dialog(){
    this.createShift();
    // this.dialogRef.close(this.params);
  }
}
