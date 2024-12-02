import { Component, inject } from '@angular/core';
import {MatSnackBar, MatSnackBarRef, MatSnackBarModule} from '@angular/material/snack-bar';

@Component({
  selector: 'app-shift-created-modal',
  templateUrl: './shift-created-modal.component.html',
  styleUrls: ['./shift-created-modal.component.css'],
  styles: [
    `
    :host {
      display: flex;
    }

    .example-pizza-party {
      color: hotpink;
    }
  `,
  ],
})
export class ShiftCreatedModalComponent {
  snackBarRef = inject(MatSnackBarRef);
}
