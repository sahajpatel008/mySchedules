import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteActionBoxComponent } from './delete-action-box.component';

describe('DeleteActionBoxComponent', () => {
  let component: DeleteActionBoxComponent;
  let fixture: ComponentFixture<DeleteActionBoxComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DeleteActionBoxComponent]
    });
    fixture = TestBed.createComponent(DeleteActionBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
