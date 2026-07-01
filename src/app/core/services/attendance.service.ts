import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Observable } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { AttendanceRecord } from '../models/attendance-record.model';

@Injectable({
  providedIn: 'root',
})
export class AttendanceService {
  private baseUrl = '/api/attendance/';

  records = signal<AttendanceRecord[]>([]);
  loading = signal<boolean>(false);
  error = signal<string | null>(null);

  constructor(private http: HttpClient) {}

  private handleError(message: string): void {
    this.error.set(message);
    this.loading.set(false);
  }

  list(date?: string, worker_id?: number): Observable<AttendanceRecord[]> {
    this.loading.set(true);
    this.error.set(null);

    let params = new HttpParams();
    if (date) {
      params = params.set('date', date);
    }
    if (worker_id !== undefined && worker_id !== null) {
      params = params.set('worker_id', worker_id.toString());
    }

    return this.http.get<AttendanceRecord[]>(this.baseUrl, { params }).pipe(
      tap((records) => {
        this.records.set(records);
        this.loading.set(false);
      }),
      catchError((error) => {
        this.handleError(error.message || 'Error loading attendance records');
        throw error;
      }),
    );
  }

  create(payload: {
    worker_id: number;
    type: AttendanceRecord['type'];
    photo: string;
    timestamp: string;
  }): Observable<AttendanceRecord> {
    this.loading.set(true);
    this.error.set(null);

    return this.http.post<AttendanceRecord>(this.baseUrl, payload).pipe(
      tap((record) => {
        this.records.update((current) => [...current, record]);
        this.loading.set(false);
      }),
      catchError((error) => {
        this.handleError(error.message || 'Error creating attendance record');
        throw error;
      }),
    );
  }

  delete(id: number): Observable<void> {
    this.loading.set(true);
    this.error.set(null);

    return this.http.delete<void>(`${this.baseUrl}${id}/`).pipe(
      tap(() => {
        this.records.update((current) => current.filter((record) => record.id !== id));
        this.loading.set(false);
      }),
      catchError((error) => {
        this.handleError(error.message || 'Error deleting attendance record');
        throw error;
      }),
    );
  }

  getCurrentShift(): 'ENTRADA' | 'SALIDA' {
    const now = new Date();
    const hours = now.getHours();
    if (hours >= 4 && hours <= 12) {
      return 'ENTRADA';
    }
    return 'SALIDA';
  }
}
