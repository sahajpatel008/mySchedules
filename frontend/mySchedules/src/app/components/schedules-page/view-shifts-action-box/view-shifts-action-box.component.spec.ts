import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewShiftsActionBoxComponent } from './view-shifts-action-box.component';

describe('ViewShiftsActionBoxComponent', () => {
  let component: ViewShiftsActionBoxComponent;
  let fixture: ComponentFixture<ViewShiftsActionBoxComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ViewShiftsActionBoxComponent]
    });
    fixture = TestBed.createComponent(ViewShiftsActionBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
