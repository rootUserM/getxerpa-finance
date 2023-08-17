import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FinanceService {

  private baseUrl = 'http://127.0.0.1:8000'; // Your Django server URL

  constructor(private http: HttpClient) { }

  getCategories(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/categories/category-expenses/`);
  }

  getCategory(id: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/categories/${id}/category-detail/`);
  }
  getTransaction(id: number): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/transactions/${id}/`);
  }
  updateTransaction(id: number,transactionData: any): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };

    return this.http.put<any>(`${this.baseUrl}/transactions/${id}/`, transactionData, httpOptions);
  }
}
