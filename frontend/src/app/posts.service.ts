import { Injectable, Input } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';

const endpoint = 'http://localhost:5000/api/';
const httpOptions = {
        headers: new HttpHeaders({
        'Content-Type':  'application/json'
  })
};

@Injectable({
  providedIn: 'root'
})

export class PostsService { 

  constructor(private http: HttpClient) { }
  
  getAllPosts(): Observable<any> {
    return this.http.get(endpoint + 'posts').pipe(
      map(this.extractData));
  }

  searchPosts(inquiry): Observable<any> {
    console.log(inquiry);
    return this.http.post<any>(endpoint + 'posts/_search', JSON.stringify(inquiry), httpOptions).pipe(
      map(this.extractData));
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
  
      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead
  
      // TODO: better job of transforming error for user consumption
      console.log(`${operation} failed: ${error.message}`);
  
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  private extractData(res: Response) {
    let body = res;
    return body || { };
  }

}
