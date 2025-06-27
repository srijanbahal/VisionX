import React, { useEffect, useState } from 'react';
import { getProcessingHistory } from '../services/api';

interface ProcessingHistoryItem {
  id: number;
  algorithm: string;
  parameters: Record<string, any>;
  created_at: string;
  original_image: string;
  processed_image: string;
}

const ProcessingHistory = () => {
  const [history, setHistory] = useState<ProcessingHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await getProcessingHistory();
        setHistory(response.history);
      } catch (error) {
        console.error('Failed to fetch history:', error);
        setError('Failed to load processing history');
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (isLoading) {
    return (
      <div className="p-4 text-center">
        <p className="text-gray-500">Loading history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-center">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="p-4 text-center">
        <p className="text-gray-500">No processing history available</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold mb-4">Processing History</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {history.map((item) => (
          <div key={item.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="p-4">
              <h3 className="font-medium text-gray-900">{item.algorithm}</h3>
              <p className="text-sm text-gray-500">
                {new Date(item.created_at).toLocaleString()}
              </p>
              <div className="mt-2 space-y-2">
                <div>
                  <p className="text-sm font-medium text-gray-700">Original</p>
                  <img
                    src={item.original_image}
                    alt="Original"
                    className="w-full h-32 object-cover rounded"
                  />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Processed</p>
                  <img
                    src={item.processed_image}
                    alt="Processed"
                    className="w-full h-32 object-cover rounded"
                  />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProcessingHistory; 