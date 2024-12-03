import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import {MatDialog} from '@angular/material/dialog';
import { PickUpShiftsComponent } from './pick-up-shifts/pick-up-shifts.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-users-dashboard',
  templateUrl: './users-dashboard.component.html',
  styleUrls: ['./users-dashboard.component.css']
})
export class UsersDashboardComponent {
  range: FormGroup;
  users: any;
  locations:any;
  availableShifts: any;
  panelOpenState = false;
  params: any;
  shiftId: any;
  userName: any;
  user: any;
  userNameFromStorage: string | null = null;
  shiftsAsPerLocation:any;


  constructor(public dialog: MatDialog, private http: HttpClient,private router: Router) {
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
    this.userNameFromStorage = localStorage.getItem('username');

  }

  // getDatesInRange(): Date[] {
  //   const startDate = this.range.value.start;
  //   const endDate = this.range.value.end;
  //   const dates: Date[] = [];

  //   if (startDate && endDate) {
  //     let currentDate = new Date(startDate);
  //     while (currentDate <= endDate) {
  //       dates.push(new Date(currentDate));
  //       currentDate.setDate(currentDate.getDate() + 1);
  //     }
  //   }

  //   return dates;
  // }
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

  getShift(){
    const apiUrl = ' http://127.0.0.1:8000/users/getShifts/';
    const headers = { 'Content-Type': 'application/json' };

    this.params = {
      start_date: this.range.value.start?.getTime(),  // Convert start date to timestamp
      end_date: this.range.value.end?.getTime() 
    }

    this.http.get(apiUrl, { params: this.params, headers }).subscribe(
      (response: any) => {
        this.availableShifts = response.data; // Assuming the backend returns a list of shifts
        this.availableShifts.forEach((element: any) => {

          console.log('this.availableShifts',this.availableShifts)
          if (element.data.length > 0) {
            element.data.forEach((shift: any) => {
              console.log('shift', shift)
              this.viewShiftsAsPerLocations(shift.location);
            
              this.shiftId = shift.shift_id;
              // this.userName = shift.user;
            });
          } 
        });
      },
      error => console.error(error)
    );
  }

  shiftPickUp(){
    console.log(this.shiftId,this.userName)

    const dialogRef = this.dialog.open(PickUpShiftsComponent, {
      panelClass: 'custom-modalbox', 
      height: '60vh',
      width: '60vw',
      data: {"shift_id": this.shiftId, "username": this.userNameFromStorage }
    });
  }

  viewShiftsAsPerLocations(shift: any){
    const apiUrl = 'http://127.0.0.1:8000/users/getShifts_allUsers/';
    const headers = { 'Content-Type': 'application/json' };
    // console.log(shift);
    this.params = {
      start_date: this.range.value.start?.getTime(), // Convert start date to timestamp
      end_date: this.range.value.end?.getTime(),
      location: shift,
    };
    // console.log(this.params)
    this.http.get(apiUrl, { params: this.params, headers }).subscribe(
      (response: any) => {
        console.log(response);
        this.shiftsAsPerLocation = response.data; // Assuming the backend returns a list of shifts
        console.log(this.shiftsAsPerLocation)
      },
      error => console.error(error)
    );
  }
  getKeys(obj: any): string[] {
    return Object.keys(obj); // Returns an array of keys, e.g., ['johndoe']
  }

  logOut(){
    this.router.navigate(['/']);
  }
}
