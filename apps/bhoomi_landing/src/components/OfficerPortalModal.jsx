import React, { useEffect, useState } from 'react';
import { X, ShieldCheck, MapPin, CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import { getOfficerQueue, submitOfficerAction } from '../api/bhoomi_api';
import { PENDING_LAND_REVIEWS } from '../data/farmStore';

export default function OfficerPortalModal({ isOpen, onClose }) {
  const [items, setItems] = useState(null);
  const [isLive, setIsLive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState(null);

  useEffect(() => {
    if (!isOpen) return;
    let cancelled = false;

    setLoading(true);
    getOfficerQueue().then((live) => {
      if (cancelled) return;
      if (live && live.length > 0) {
        setItems(live);
        setIsLive(true);
      } else {
        setItems(PENDING_LAND_REVIEWS);
        setIsLive(false);
      }
      setLoading(false);
    });

    return () => {
      cancelled = true;
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const handleAction = async (item, action) => {
    const id = item.parcel_id || item.id;
    setBusyId(id);
    if (isLive) {
      await submitOfficerAction(item.parcel_id, action, 'Reviewed via Bhoomi landing preview');
      const refreshed = await getOfficerQueue();
      if (refreshed) setItems(refreshed);
    } else {
      setItems((prev) =>
        prev.map((p) => (p.id === id ? { ...p, status: action === 'verified' ? 'Verified' : 'Rejected' } : p))
      );
    }
    setBusyId(null);
  };

  return (
    <div className="fixed inset-0 z-50 flex flex-col text-slate-900 animate-fade-in bg-white overflow-hidden">
      <div className="absolute top-4 right-6 z-[60]">
        <button
          onClick={onClose}
          className="p-2 rounded-full bg-white shadow-md border border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-50 transition-colors"
          title="Close Dashboard"
        >
          <X className="w-6 h-6" />
        </button>
      </div>

      <div className="flex-grow w-full h-full overflow-y-auto bg-slate-50">
        <div className="max-w-4xl mx-auto px-6 py-16 space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-100 border border-blue-300 flex items-center justify-center">
              <ShieldCheck className="w-5 h-5 text-blue-700" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">Revenue Officer — Land Verification Queue</h2>
              <p className="text-sm text-slate-500">
                {loading
                  ? 'Loading queue…'
                  : isLive
                    ? 'Live data from the Bhoomi API (GET /api/v1/officer/queue)'
                    : 'Backend unreachable — showing bundled demo data'}
              </p>
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-20 text-slate-400">
              <Loader2 className="w-6 h-6 animate-spin" />
            </div>
          ) : (
            <div className="space-y-3">
              {items.map((item) => {
                const id = item.parcel_id || item.id;
                const farmerName = item.farmer_name || item.farmerName;
                const village = item.village;
                const surveyNumber = item.survey_number || item.surveyNumber;
                const status = item.status;
                const isResolved = status === 'verified' || status === 'Verified' || status === 'rejected' || status === 'Rejected';

                return (
                  <div key={id} className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="font-bold text-slate-900">{farmerName}</p>
                        <p className="text-xs text-slate-500 flex items-center gap-1 mt-1">
                          <MapPin className="w-3.5 h-3.5" /> {village} · Survey No. {surveyNumber}
                        </p>
                      </div>
                      <span
                        className={`text-[10px] font-bold px-2 py-1 rounded-full uppercase ${
                          isResolved
                            ? status.toLowerCase() === 'verified'
                              ? 'bg-emerald-100 text-emerald-700'
                              : 'bg-rose-100 text-rose-700'
                            : 'bg-amber-100 text-amber-700'
                        }`}
                      >
                        {status}
                      </span>
                    </div>

                    {!isResolved && (
                      <div className="flex gap-2 mt-4">
                        <button
                          onClick={() => handleAction(item, 'verified')}
                          disabled={busyId === id}
                          className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-xl bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-700 disabled:opacity-50"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5" /> Verify
                        </button>
                        <button
                          onClick={() => handleAction(item, 'rejected')}
                          disabled={busyId === id}
                          className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-xl bg-rose-100 text-rose-700 text-xs font-bold hover:bg-rose-200 disabled:opacity-50"
                        >
                          <XCircle className="w-3.5 h-3.5" /> Reject
                        </button>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
