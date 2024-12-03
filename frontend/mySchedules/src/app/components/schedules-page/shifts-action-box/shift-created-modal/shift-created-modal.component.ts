import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-shift-created-modal',
  templateUrl: './shift-created-modal.component.html',
  styleUrls: ['./shift-created-modal.component.css'],
})
export class ShiftCreatedModalComponent {

  constructor(public dialogRef: MatDialogRef<ShiftCreatedModalComponent>){}
  
  closeDialog() {
    this.dialogRef.close();
  }

}
