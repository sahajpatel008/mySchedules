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

  constructor(
    public dialogRef: MatDialogRef<ShiftsActionBoxComponent>,
    private http: HttpClient
  ) {}

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

  closeDialog() {
    this.dialogRef.close('closed!');
  }

}
