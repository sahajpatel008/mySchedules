import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShiftsActionBoxComponent } from './shifts-action-box.component';

describe('ShiftsActionBoxComponent', () => {
  let component: ShiftsActionBoxComponent;
  let fixture: ComponentFixture<ShiftsActionBoxComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ShiftsActionBoxComponent]
    });
    fixture = TestBed.createComponent(ShiftsActionBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
