<div className="mt-4 flex flex-wrap gap-4 text-xs text-gray-500 border-t pt-4">
  <div>
    <span className="font-semibold text-gray-700 block">Type</span>
    {caseData.disruption_details?.disruption_type || 'N/A'}
  </div>
  <div>
    <span className="font-semibold text-gray-700 block">Location</span>
    <div className="flex items-center gap-1">
      {caseData.structured_context?.location_code && (
        <Badge variant="outline" className="text-[10px] font-mono h-4 px-1">{caseData.structured_context.location_code}</Badge>
      )}
      {caseData.disruption_details?.identifier || 'N/A'}
    </div>
  </div>
  <div>
    <span className="font-semibold text-gray-700 block">Carrier</span>
    <div className="flex items-center gap-1">
      {caseData.structured_context?.carrier_code && (
        <Badge variant="outline" className="text-[10px] font-mono h-4 px-1">{caseData.structured_context.carrier_code}</Badge>
      )}
      {caseData.shipment_identifiers?.carriers?.[0] || 'N/A'}
    </div>
  </div>
</div>