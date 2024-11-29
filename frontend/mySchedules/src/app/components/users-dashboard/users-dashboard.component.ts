import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import {MatDialog} from '@angular/material/dialog';

@Component({
  selector: 'app-users-dashboard',
  templateUrl: './users-dashboard.component.html',
  styleUrls: ['./users-dashboard.component.css']
})
export class UsersDashboardComponent {
  range: FormGroup;
  users: any;
  locations:any;
  
  panelOpenState = false;
  
  constructor(public dialog: MatDialog) {
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
  }

  getDatesInRange(): Date[] {
    const startDate = this.range.value.start;
    const endDate = this.range.value.end;
    const dates: Date[] = [];

    if (startDate && endDate) {
      let currentDate = new Date(startDate);
      while (currentDate <= endDate) {
        dates.push(new Date(currentDate));
        currentDate.setDate(currentDate.getDate() + 1);
      }
    }

    return dates;
  }
}
