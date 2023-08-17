import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FinanceService } from '../finance.service';

@Component({
  selector: 'app-category-detail',
  templateUrl: './category-detail.component.html',
  styleUrls: ['./category-detail.component.css']
})
export class CategoryDetailComponent {
  cat_transaction: any;

  constructor(private route: ActivatedRoute, private financeService: FinanceService) { }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const categoryId = params.get('id');
      if (categoryId) {
        this.financeService.getCategory(Number(categoryId)).subscribe(
          (data) => {
            this.cat_transaction = data;
            console.log(this.cat_transaction)
          },
          (error) => {
            console.error('Error fetching category by ID:', error);
          }
        );
      }
    });
  }
}
