export type RecordType = 'ENTRADA' | 'SALIDA';

export interface AttendanceRecord {
  id?: number;
  worker_id: number;
  worker_name: string;
  type: RecordType;
  time: string;
  date: string;
  date_iso: string;
  photo: string;       // base64 o URL
  timestamp: string;
}
