import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShiftCreatedModalComponent } from './shift-created-modal.component';

describe('ShiftCreatedModalComponent', () => {
  let component: ShiftCreatedModalComponent;
  let fixture: ComponentFixture<ShiftCreatedModalComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShiftCreatedModalComponent]
    });
    fixture = TestBed.createComponent(ShiftCreatedModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
