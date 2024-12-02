import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import {FormControl, Validators, FormBuilder, FormGroup, AbstractControl, ValidationErrors} from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-up-page',
  templateUrl: './sign-up-page.component.html',
  styleUrls: ['./sign-up-page.component.css']
})
export class SignUpPageComponent {
  
  email = new FormControl('', [Validators.required, Validators.email]);

  registerForm: FormGroup;
  data: any;

  constructor(private fb: FormBuilder, private http: HttpClient,private router: Router) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required],
    },
    { validators: this.passwordMatchValidator });
  }
  
  getErrorMessage() {
    if (this.email.hasError('required')) {
      return 'You must enter a value';
    }

    return this.email.hasError('email') ? 'Not a valid email' : '';
  }
  hide = true;

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password')?.value;
    const confirmPassword = control.get('confirmPassword')?.value;

    if (password && confirmPassword && password !== confirmPassword) {
      control.get('confirmPassword')?.setErrors({ mismatch: true }); // Set mismatch error
      return { mismatch: true };
    } else {
      control.get('confirmPassword')?.setErrors(null); // Clear errors if they match
      return null;
    }
  }

  onRegister() : void | any{
    if (this.registerForm.valid) {
      const apiUrl = 'http://127.0.0.1:8000/users/register/';

      const headers = { 'Content-Type': 'application/json' };
      const body = JSON.stringify(this.registerForm.value);

      this.http.post(apiUrl, body, { headers }).subscribe(
        response => console.log(response),
        error => console.error(error)
      );
      this.router.navigate(['/']);
    }    
  }
}