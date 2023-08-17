import { Component } from '@angular/core';
import { FinanceService } from '../finance.service';
import { ActivatedRoute } from '@angular/router';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-transaction-detail',
  templateUrl: './transaction-detail.component.html',
  styleUrls: ['./transaction-detail.component.css']
})
export class TransactionDetailComponent {
  transaction: any;
  checked = false;

  constructor(private route: ActivatedRoute, private financeService: FinanceService) { }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const categoryId = params.get('id');
      if (categoryId) {
        this.financeService.getTransaction(Number(categoryId)).subscribe(
          (data) => {
            this.transaction = data;
            console.log(this.transaction)
          },
          (error) => {
            console.error('Error fetching category by ID:', error);
          }
        );
      }
    });
  }
  toggleAction(event: MatSlideToggleChange) {
    const isChecked = event.checked;
    const transactionData = { "id":this.transaction.id, "description": this.transaction.description, "category": this.transaction.category, "amount": this.transaction.amount, "ignore": isChecked}
    this.financeService.updateTransaction(this.transaction.id,transactionData)
      .subscribe(
        (response: any) => {
          console.log('Transaction updated:', response);
        },
        (error: HttpErrorResponse) => {
          console.error('Error updating transaction:', error);
        }
      );
  }

}
