import { Component,OnInit } from '@angular/core';
import { FinanceService } from '../finance.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit{
  categories: any[] = [];

  constructor(private financeService: FinanceService) { }

  ngOnInit() {
    this.financeService.getCategories().subscribe(
      (data) => {
        this.categories = data;
        console.log(this.categories)
      },
      (error) => {
        console.error('Error fetching items:', error);
      }
    );
  }
}
