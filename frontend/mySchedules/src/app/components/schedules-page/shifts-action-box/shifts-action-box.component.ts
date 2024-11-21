import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-shifts-action-box',
  templateUrl: './shifts-action-box.component.html',
  styleUrls: ['./shifts-action-box.component.css']
})
export class ShiftsActionBoxComponent {

  constructor(public dialogRef: MatDialogRef<ShiftsActionBoxComponent>) {}

  closeDialog() {
    this.dialogRef.close('Pizza!');
  }

}
