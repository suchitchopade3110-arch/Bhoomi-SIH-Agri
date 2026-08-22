class GeoJsonPolygonData {
  final String type;
  final List<List<List<double>>> coordinates;

  const GeoJsonPolygonData({
    this.type = 'Polygon',
    required this.coordinates,
  });

  Map<String, dynamic> toJson() => {
        'type': type,
        'coordinates': coordinates,
      };

  factory GeoJsonPolygonData.fromJson(Map<String, dynamic> json) {
    final rawCoords = json['coordinates'] as List? ?? [];
    final parsed = rawCoords.map<List<List<double>>>((ring) {
      return (ring as List).map<List<double>>((pt) {
        return (pt as List).map<double>((c) => (c as num).toDouble()).toList();
      }).toList();
    }).toList();

    return GeoJsonPolygonData(
      type: json['type'] as String? ?? 'Polygon',
      coordinates: parsed,
    );
  }
}

class LandSubmissionRequest {
  final String surveyNo;
  final double areaAcres;
  final GeoJsonPolygonData? boundaryGeojson;

  const LandSubmissionRequest({
    required this.surveyNo,
    required this.areaAcres,
    this.boundaryGeojson,
  });

  Map<String, dynamic> toJson() => {
        'survey_no': surveyNo,
        'area_acres': areaAcres,
        if (boundaryGeojson != null) 'boundary_geojson': boundaryGeojson!.toJson(),
      };
}
