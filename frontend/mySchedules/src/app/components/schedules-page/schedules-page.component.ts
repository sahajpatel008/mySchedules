import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ShiftsActionBoxComponent } from './shifts-action-box/shifts-action-box.component';
import { ViewShiftsActionBoxComponent } from './view-shifts-action-box/view-shifts-action-box.component';
import {MatDialog} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-schedules-page',
  templateUrl: './schedules-page.component.html',
  styleUrls: ['./schedules-page.component.css']
})
export class SchedulesPageComponent implements OnInit{
  range: FormGroup;
  users: any;
  users_shift: any;
  locations:any;
  shiftDetails: any;
  shiftId: number | undefined;
  shift_status: any;
  shifts: any;
  panelOpenState = false;
  params: any;
  startDate: any;
  endDate: any;
  dateRange: any;
  shiftDataByDate: { [key: string]: any[] } = {};
  shiftData:any;
  shiftsAsPerLocation:any;

  constructor(public dialog: MatDialog,
    private http: HttpClient,
    private router: Router) {
    // Initialize the range form group with null values
    this.range = new FormGroup({
      start: new FormControl<Date | null>(null),
      end: new FormControl<Date | null>(null),
    });
  }

  ngOnInit(): void {
    const today = new Date();
    const startOfWeek = new Date(today);
    const endOfWeek = new Date(today);

    // Set start to the most recent Monday
    startOfWeek.setDate(today.getDate() - today.getDay() + 1);

    // Set end to the upcoming Sunday
    endOfWeek.setDate(startOfWeek.getDate() + 6);

    // Set default values for the date range
    this.range.setValue({
      start: startOfWeek,
      end: endOfWeek,
    });

    if (this.shiftId) {
      this.getEmployeesByShiftId(this.shiftId);
    }

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

    this.getShift();
    this.range.valueChanges.subscribe(() => {
      console.log(1)
      this.getShift();
    });

  }
  
  getDatesInRange(): Date[] {
    const start = this.range.get('start')?.value;
    const end = this.range.get('end')?.value;
  
    const dates: Date[] = [];
    if (start && end) {
      const startDate = new Date(start);
      const endDate = new Date(end);
  
      for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
        dates.push(new Date(d));
      }
    }
    return dates;
  }
  
  formatDate(date: Date): string {
    return date.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit', day: '2-digit' });
  }
  
  addShift(user: any) {
    const dialogRef = this.dialog.open(ShiftsActionBoxComponent, {
      panelClass: 'custom-modalbox',
      height: '60vh',
      width: '60vw'
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.shiftDetails = result;
  
        // Prepare the final structure
        const finalJSON: { dates: { date: string, data: any[] }[] } = { dates: [] };
  
        // Iterate over all dates in the range and initialize
        this.getDatesInRange().forEach(date => {
          finalJSON.dates.push({
            date: this.formatDate(new Date(date)),
            data: []
          });
        });
  
        // Add the shift details to the matching date
        const shiftDateKey = this.formatDate(new Date(this.shiftDetails.date));
        const dateEntry = finalJSON.dates.find(entry => entry.date === shiftDateKey);
  
        if (dateEntry) {
          dateEntry.data.push({
            user: user.name,
            location: this.shiftDetails.location,
            start_time: this.shiftDetails.start_time,
            end_time: this.shiftDetails.end_time
          });
        }
  
        this.shiftData = finalJSON;
  
        // Log the final JSON object
        console.log('Final JSON:', this.shiftData);
      }
    });
  }
  
  getShift(){
    const apiUrl = 'http://127.0.0.1:8000/users/getShifts/';
    const headers = { 'Content-Type': 'application/json' };

    this.params = {
      start_date: this.range.value.start?.getTime(), // Convert start date to timestamp
      end_date: this.range.value.end?.getTime(),
    };

    this.http.get(apiUrl, { params: this.params, headers }).subscribe(
      (response: any) => {
        console.log(response)
        this.shifts = response.data; // Assuming the backend returns a list of shifts
        console.log(this.shifts)
      },
      error => console.error(error)
    );
    let shiftId,userName
    this.shifts.forEach((ele: any) =>{
      shiftId = ele.shift_id;
      userName = ele.user;
    })
    this.requestedShifts(shiftId, userName)
  }
  
  getEmployeesByShiftId(shiftId: number): void {
    const dialogRef = this.dialog.open(ViewShiftsActionBoxComponent, {
      panelClass: 'custom-modalbox', 
      height: '60vh',
      width: '60vw',
      data: { "username":this.users_shift, "shift_id": shiftId, "status": this.shift_status }
    });
  }
  requestedShifts(shiftId: any, userName: any){
    const apiUrl = 'http://127.0.0.1:8000/users/getPickupRequests/';
    const headers = { 'Content-Type': 'application/json' };

    this.params = {
      start_date: this.range.value.start?.getTime(), // Convert start date to timestamp
      end_date: this.range.value.end?.getTime(),
      userName,
      shiftId
    };

    this.http.get(apiUrl, { params: this.params, headers }).subscribe(
      (response: any) => {
        this.shifts = response.shifts; // Assuming the backend returns a list of shifts
        console.log(this.shifts)
      },
      error => console.error(error)
    );
  }
  logOut(){
    this.router.navigate(['/']);
  }

  viewShiftsAsPerLocations(){
    let shift_location;
    console.log(this.shifts)
    this.shifts.forEach((ele: any) => {
      shift_location = ele.shift_id
    });

    const apiUrl = 'http://127.0.0.1:8000/users/getShifts_allUsers/';
    const headers = { 'Content-Type': 'application/json' };

    this.params = {
      start_date: this.range.value.start?.getTime(), // Convert start date to timestamp
      end_date: this.range.value.end?.getTime(),
      location: shift_location,
    };
    console.log(this.params)
    this.http.post(apiUrl, { params: this.params, headers }).subscribe(
      (response: any) => {
        this.shiftsAsPerLocation = response.shifts; // Assuming the backend returns a list of shifts
        console.log(this.shiftsAsPerLocation)
      },
      error => console.error(error)
    );
  }
  getKeys(obj: any): string[] {
    console.log(obj)
    return Object.keys(obj); // Returns an array of keys, e.g., ['johndoe']
  }
  
}
