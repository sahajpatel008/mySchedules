import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MatButtonModule } from '@angular/material/button';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SchedulesPageComponent } from './components/schedules-page/schedules-page.component';
import { RouterModule } from '@angular/router';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { ShiftsActionBoxComponent } from './components/schedules-page/shifts-action-box/shifts-action-box.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatExpansionModule } from '@angular/material/expansion';
import {MatTabsModule} from '@angular/material/tabs';
import {NgFor} from '@angular/common';
import {MatSelectModule} from '@angular/material/select';
import { HttpClientModule } from '@angular/common/http';
import { SignUpPageComponent } from './components/sign-up-page/sign-up-page.component';
import { UsersDashboardComponent } from './components/users-dashboard/users-dashboard.component';
import { ViewShiftsActionBoxComponent } from './components/schedules-page/view-shifts-action-box/view-shifts-action-box.component';
import { PickUpShiftsComponent } from './components/users-dashboard/pick-up-shifts/pick-up-shifts.component';
import { ShiftCreatedModalComponent } from './components/schedules-page/shifts-action-box/shift-created-modal/shift-created-modal.component';
import {MatMenuModule} from '@angular/material/menu';
import { DeleteActionBoxComponent } from './components/schedules-page/delete-action-box/delete-action-box.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginPageComponent,
    SchedulesPageComponent,
    ShiftsActionBoxComponent,
    SignUpPageComponent,
    UsersDashboardComponent,
    ViewShiftsActionBoxComponent,
    PickUpShiftsComponent,
    ShiftCreatedModalComponent,
    DeleteActionBoxComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    RouterModule,
    MatDatepickerModule, MatNativeDateModule,
    FormsModule, 
    MatDialogModule,
    MatIconModule,
    MatExpansionModule,
    MatTabsModule,
    MatMenuModule,
    MatSelectModule, NgFor,HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
