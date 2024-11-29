import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SchedulesPageComponent } from './components/schedules-page/schedules-page.component';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { SignUpPageComponent } from './components/sign-up-page/sign-up-page.component';
import { UsersDashboardComponent } from './components/users-dashboard/users-dashboard.component';

const routes: Routes = [
  {
    path: '',
    component: LoginPageComponent
  },
  {
    path: 'schedulesPage',
    component: SchedulesPageComponent
  },
  {
    path: 'signUpPage',
    component: SignUpPageComponent
  },
  {
    path: 'UsersDashboard',
    component: UsersDashboardComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
