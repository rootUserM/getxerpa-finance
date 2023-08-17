import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-margin-wrapper',
  template: `
    <div [style.margin]="margin">
      <ng-content></ng-content>
    </div>
  `,
  styles: []
})
export class MarginWrapperComponent {
  @Input() margin = '16px'; // Default margin value
}
