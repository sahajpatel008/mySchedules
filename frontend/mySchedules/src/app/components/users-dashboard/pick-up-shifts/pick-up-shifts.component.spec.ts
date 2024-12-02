import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PickUpShiftsComponent } from './pick-up-shifts.component';

describe('PickUpShiftsComponent', () => {
  let component: PickUpShiftsComponent;
  let fixture: ComponentFixture<PickUpShiftsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PickUpShiftsComponent]
    });
    fixture = TestBed.createComponent(PickUpShiftsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
