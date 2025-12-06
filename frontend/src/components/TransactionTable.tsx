import React from 'react';
import type { Transaction } from '../types';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { cn } from '@/lib/utils';

interface TransactionTableProps {
  transactions: Transaction[];
  className?: string;
}

export const TransactionTable: React.FC<TransactionTableProps> = ({ transactions, className }) => {
  if (transactions.length === 0) {
    return (
      <Card className={className}>
        <CardContent className="p-6 text-center text-muted-foreground">
          No transactions to display.
        </CardContent>
      </Card>
    );
  }

  // Calculate totals
  const totalDebit = transactions.reduce((sum, t) => sum + t.debit, 0);
  const totalCredit = transactions.reduce((sum, t) => sum + t.credit, 0);

  return (
    <Card className={cn("overflow-hidden", className)}>
      <CardHeader className="bg-muted/50 pb-4">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Extracted Transactions ({transactions.length})</CardTitle>
          <div className="flex space-x-4 text-sm font-medium">
            <div className="text-red-500">Total Debit: {totalDebit.toFixed(2)}</div>
            <div className="text-green-500">Total Credit: {totalCredit.toFixed(2)}</div>
          </div>
        </div>
      </CardHeader>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="bg-muted text-muted-foreground uppercase text-xs">
            <tr>
              <th className="px-6 py-3 font-medium">Date</th>
              <th className="px-6 py-3 font-medium">Description</th>
              <th className="px-6 py-3 font-medium text-right">Debit</th>
              <th className="px-6 py-3 font-medium text-right">Credit</th>
              <th className="px-6 py-3 font-medium text-right">Balance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {transactions.map((txn, index) => (
              <tr key={index} className="hover:bg-muted/50 transition-colors">
                <td className="px-6 py-3 whitespace-nowrap">
                  {new Date(txn.date).toLocaleDateString()}
                </td>
                <td className="px-6 py-3 max-w-md truncate" title={txn.description}>
                  {txn.description}
                </td>
                <td className="px-6 py-3 text-right font-mono text-red-600">
                  {txn.debit > 0 ? txn.debit.toFixed(2) : '-'}
                </td>
                <td className="px-6 py-3 text-right font-mono text-green-600">
                  {txn.credit > 0 ? txn.credit.toFixed(2) : '-'}
                </td>
                <td className="px-6 py-3 text-right font-mono text-foreground font-medium">
                  {txn.balance.toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
};
