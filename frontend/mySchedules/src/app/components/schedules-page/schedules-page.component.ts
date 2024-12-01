import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ShiftsActionBoxComponent } from './shifts-action-box/shifts-action-box.component';
import { ViewShiftsActionBoxComponent } from './view-shifts-action-box/view-shifts-action-box.component';
import {MatDialog} from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-schedules-page',
  templateUrl: './schedules-page.component.html',
  styleUrls: ['./schedules-page.component.css']
})
export class SchedulesPageComponent implements OnInit{
  range: FormGroup;
  users: any;
  locations:any;
  shiftDetails: any;
  shiftId: number | undefined;
  shifts: any[] = [];
  panelOpenState = false;
  params: any;
  startDate: any;
  endDate: any;

  constructor(public dialog: MatDialog,private http: HttpClient) {
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
      this.getShift();
    });
  }

  getDatesInRange(): Date[] {
   this.startDate = this.range.value.start;
    this.endDate = this.range.value.end;
    const dates: Date[] = [];

    if (this.startDate && this.endDate) {
      let currentDate = new Date(this.startDate);
      while (currentDate <= this.endDate) {
        dates.push(new Date(currentDate));
        currentDate.setDate(currentDate.getDate() + 1);
      }
    }    

    return dates;
  }

  addShift(user: any){
    const dialogRef = this.dialog.open(ShiftsActionBoxComponent,{
      panelClass: 'custom-modalbox', 
      height: '60vh',
      width: '60vw'
    });
   
    dialogRef.afterClosed().subscribe(result => {
      this.shiftDetails = result;
      console.log('Dialog result:', result);
    });
  }

  // viewShift(shiftId: number) {
  //   const dialogRef = this.dialog.open(ViewShiftsActionBoxComponent, {
  //     panelClass: 'custom-modalbox', 
  //     height: '60vh',
  //     width: '60vw',
  //     data: { shiftId }
  //   });
  
  //   dialogRef.afterClosed().subscribe(result => {
  //     console.log('Dialog closed', result);
  //   });
  // }

  getShift() {
    const apiUrl = 'http://127.0.0.1:8000/users/getShifts/';
    const headers = { 'Content-Type': 'application/json' };

    this.params = {
      start_date: this.range.value.start?.getTime(), // Convert start date to timestamp
      end_date: this.range.value.end?.getTime(),
    };

    console.log(this.params);
    this.http.get(apiUrl, { params: this.params, headers }).subscribe(
      (response: any) => {
        this.shifts = response.shifts; // Assuming the backend returns a list of shifts
      },
      error => console.error(error)
    );
  }
  
  getEmployeesByShiftId(shiftId: number): void {
    const apiUrl = `http://127.0.0.1:8000/users/getPickupRequests/`; // Example API endpoint
    const headers = { 'Content-Type': 'application/json' };
    const body = { shift_id: shiftId }; // Send the shift ID in JSON format

    this.http.post(apiUrl, body, { headers }).subscribe(
      (response: any) => {
        this.users = response.shift.employee.username || [];
      },
      error => {
        console.error('Error fetching shift requests:', error);
      }
    );

    const dialogRef = this.dialog.open(ViewShiftsActionBoxComponent, {
      panelClass: 'custom-modalbox', 
      height: '60vh',
      width: '60vw',
      data: { shiftId }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('Dialog closed', result);
    });
  }
}
