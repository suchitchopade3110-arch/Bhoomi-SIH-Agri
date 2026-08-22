import React, { useState } from 'react';
import { useLandQueue } from '../hooks/use_land_queue';
import { Badge } from '../../../components/ui/badge';
import { BoundaryMap } from '../components/boundary_map';
import { Archive, Search, MapPin, Calendar } from 'lucide-react';

export const VerifiedArchivePage: React.FC = () => {
  const { data: queueItems = [] } = useLandQueue();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLandId, setSelectedLandId] = useState<string | null>(null);

  // Filter verified and rejected items
  const archiveItems = queueItems.filter(
    (item) => item.status === 'verified' || item.status === 'rejected'
  );

  const filteredItems = archiveItems.filter(
    (item) =>
      item.farmer_stated.survey_no.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.farm_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.land_record_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const selectedItem =
    archiveItems.find((i) => i.land_record_id === selectedLandId) || filteredItems[0] || null;

  return (
    <div className="flex h-[calc(100vh-4rem)] w-full overflow-hidden bg-slate-50/50">
      {/* Left List */}
      <div className="flex h-full w-full max-w-sm flex-col border-r border-slate-200 bg-white">
        <div className="border-b border-slate-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Archive className="h-4 w-4 text-[#2E7D32]" />
              <h2 className="text-sm font-black text-slate-900">Verified Archive</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-bold text-slate-600">
              {filteredItems.length} records
            </span>
          </div>
          <p className="mt-1 text-[11px] text-slate-500">
            Historical approved and rejected parcel decisions
          </p>

          <div className="relative mt-3">
            <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search survey no, farm ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-1.5 pl-8 pr-3 text-xs focus:border-[#2E7D32] focus:bg-white focus:outline-none"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2.5">
          {filteredItems.length === 0 ? (
            <div className="flex h-48 flex-col items-center justify-center text-center text-slate-400">
              <Archive className="h-8 w-8 text-slate-300" />
              <p className="mt-2 text-xs font-medium">No archived records found</p>
            </div>
          ) : (
            filteredItems.map((item) => {
              const isSelected = selectedItem?.land_record_id === item.land_record_id;
              return (
                <div
                  key={item.land_record_id}
                  onClick={() => setSelectedLandId(item.land_record_id)}
                  className={`cursor-pointer rounded-xl border p-3.5 transition-all ${
                    isSelected
                      ? 'border-[#2E7D32] bg-[#2E7D32]/5 shadow-xs'
                      : 'border-slate-200/80 bg-white hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-slate-900">
                      Survey No: {item.farmer_stated.survey_no}
                    </span>
                    <Badge variant={item.status === 'verified' ? 'verified' : 'neutral'}>
                      {item.status === 'verified' ? 'Verified' : 'Rejected'}
                    </Badge>
                  </div>
                  <div className="mt-1.5 flex items-center justify-between text-[11px] text-slate-500">
                    <span>Farm ID: {item.farm_id}</span>
                    <span>{item.farmer_stated.area_acres} Acres</span>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Right Detail & Map */}
      <div className="flex-1 overflow-y-auto p-6 lg:p-8 space-y-6">
        {selectedItem ? (
          <>
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
              <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xl font-extrabold text-slate-900">
                      Survey No. {selectedItem.farmer_stated.survey_no}
                    </h2>
                    <Badge variant={selectedItem.status === 'verified' ? 'verified' : 'neutral'}>
                      {selectedItem.status === 'verified' ? 'Official Verified' : 'Rejected Decision'}
                    </Badge>
                  </div>
                  <p className="mt-0.5 text-xs text-slate-500">
                    Land Record ID: <span className="font-mono">{selectedItem.land_record_id}</span>
                  </p>
                </div>

                <div className="flex items-center gap-2 rounded-xl bg-slate-50 p-2 text-xs text-slate-600 border border-slate-200/60">
                  <Calendar className="h-4 w-4 text-slate-400" />
                  <span>Submitted: {new Date(selectedItem.submitted_at).toLocaleDateString()}</span>
                </div>
              </div>

              <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                <div className="rounded-xl bg-slate-50 p-3">
                  <span className="text-slate-400 block text-[10px] font-bold uppercase">Land Area</span>
                  <span className="text-sm font-extrabold text-slate-800">{selectedItem.farmer_stated.area_acres} Acres</span>
                </div>
                <div className="rounded-xl bg-slate-50 p-3">
                  <span className="text-slate-400 block text-[10px] font-bold uppercase">Farm Identifier</span>
                  <span className="text-sm font-extrabold text-slate-800">{selectedItem.farm_id}</span>
                </div>
                <div className="rounded-xl bg-slate-50 p-3">
                  <span className="text-slate-400 block text-[10px] font-bold uppercase">Verification Status</span>
                  <span className={`text-sm font-extrabold ${selectedItem.status === 'verified' ? 'text-emerald-700' : 'text-red-700'}`}>
                    {selectedItem.status.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>

            {/* Boundary Map */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-[#2E7D32]" />
                  <h3 className="text-sm font-bold text-slate-800">
                    Spatial Polygon Record (OpenStreetMap)
                  </h3>
                </div>
                <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-slate-600">
                  GeoJSON Polygon
                </span>
              </div>

              <BoundaryMap
                boundaryGeojson={selectedItem.boundary_geojson}
                surveyNo={selectedItem.farmer_stated.survey_no}
                areaAcres={selectedItem.farmer_stated.area_acres}
              />
            </div>
          </>
        ) : (
          <div className="flex h-full flex-col items-center justify-center text-center text-slate-400">
            <Archive className="h-12 w-12 text-slate-300" />
            <h3 className="mt-3 text-base font-bold text-slate-800">No Record Selected</h3>
            <p className="mt-1 text-xs text-slate-500">
              Select an archived parcel record to inspect spatial boundaries and verification status.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
