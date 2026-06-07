import { useState, useEffect } from 'react';
import { TrendingUp, Loader2 } from 'lucide-react';
import { TrendItem } from '../components/TrendItem';
import { getTrendingClaims, type TrendingClaim } from '../services/api';

interface TrendsPageProps {
  onNavigate: (page: 'claim-details', claimId: string) => void;
}

export function TrendsPage({ onNavigate }: TrendsPageProps) {
  const [trends, setTrends] = useState<TrendingClaim[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTrends();
  }, []);

  const loadTrends = async () => {
    try {
      setLoading(true);
      const data = await getTrendingClaims();
      setTrends(data);
    } catch (error) {
      console.error('Error loading trends:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-pink-500 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-gray-900">Trending Claims</h1>
              <p className="text-gray-600">What students are verifying right now</p>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
          </div>
        )}

        {/* Trends List */}
        {!loading && trends.length > 0 && (
          <div className="space-y-4">
            {trends.map((trend) => (
              <TrendItem
                key={trend.id}
                claim={trend}
                onClick={() => onNavigate('claim-details', trend.id)}
              />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && trends.length === 0 && (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-gray-900 mb-2">No trending claims yet</h3>
            <p className="text-gray-600">Check back soon for popular verifications!</p>
          </div>
        )}
      </div>
    </div>
  );
}
