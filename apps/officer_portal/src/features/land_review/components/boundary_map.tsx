import React from 'react';
import { MapContainer, TileLayer, Polygon, Marker, Popup } from 'react-leaflet';
import { GeoJSONPolygon } from '../types/land.types';
import L from 'leaflet';

// Fix default Leaflet icon paths
const customIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

interface BoundaryMapProps {
  boundaryGeojson?: GeoJSONPolygon | null;
  surveyNo: string;
  areaAcres: number;
}

export const BoundaryMap: React.FC<BoundaryMapProps> = ({
  boundaryGeojson,
  surveyNo,
  areaAcres,
}) => {
  if (!boundaryGeojson || !boundaryGeojson.coordinates || boundaryGeojson.coordinates.length === 0) {
    return (
      <div className="flex h-64 w-full items-center justify-center rounded-xl border border-dashed border-slate-200 bg-slate-50 text-xs text-slate-400">
        No boundary GeoJSON coordinates provided for this parcel.
      </div>
    );
  }

  // Convert GeoJSON [lng, lat] coordinates to Leaflet [lat, lng]
  const rawRing = boundaryGeojson.coordinates[0] || [];
  const leafletCoords: [number, number][] = rawRing.map((pt) => [pt[1], pt[0]]);

  // Calculate center of polygon
  const centerLat = leafletCoords.reduce((acc, curr) => acc + curr[0], 0) / leafletCoords.length || 11.3412;
  const centerLng = leafletCoords.reduce((acc, curr) => acc + curr[1], 0) / leafletCoords.length || 77.7214;
  const centerPosition: [number, number] = [centerLat, centerLng];

  return (
    <div className="relative isolate h-72 w-full overflow-hidden rounded-xl border border-slate-200 shadow-sm z-0">
      <MapContainer
        center={centerPosition}
        zoom={15}
        scrollWheelZoom={false}
        className="h-full w-full z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Boundary Polygon */}
        <Polygon
          positions={leafletCoords}
          pathOptions={{
            color: '#2E7D32',
            fillColor: '#66B86A',
            fillOpacity: 0.35,
            weight: 3,
          }}
        />

        {/* Center Pin */}
        <Marker position={centerPosition} icon={customIcon}>
          <Popup>
            <div className="text-xs">
              <strong>Survey No: {surveyNo}</strong>
              <br />
              Area: {areaAcres} Acres
            </div>
          </Popup>
        </Marker>
      </MapContainer>

      {/* Map Header Floating Overlay */}
      <div className="absolute top-3 left-3 z-10 rounded-lg bg-white/90 px-2.5 py-1 text-[11px] font-bold text-slate-800 shadow-sm backdrop-blur-xs border border-slate-200 pointer-events-none">
        <span>Survey No: {surveyNo} &bull; {areaAcres} Acres</span>
      </div>
    </div>
  );
};
