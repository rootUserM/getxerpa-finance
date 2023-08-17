import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-centered-card',
  template: `
    <div fxLayout="column" fxLayoutAlign="center center" style="height: 100vh;">
      <mat-card>
        <ng-content></ng-content>
      </mat-card>
    </div>
  `,
  styles: []
})
export class CenteredCardComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
