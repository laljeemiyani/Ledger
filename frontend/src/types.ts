export interface Transaction {
  date: string;
  description: string;
  debit: number;
  credit: number;
  balance: number;
  reference_no?: string;
  value_date?: string;
}

export interface ProcessingResult {
  file: string;
  status: 'success' | 'error';
  bank?: string;
  transaction_count?: number;
  transactions?: Transaction[];
  message?: string;
}
