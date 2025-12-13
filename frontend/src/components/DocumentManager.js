import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, FileText, Upload, AlertTriangle, CheckCircle2, GitCompare, Eye } from "lucide-react";
import { toast } from "sonner";
import api from '../services/api';

const DocumentManager = ({ caseId }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [comparing, setComparing] = useState(false);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [selectedDocs, setSelectedDocs] = useState([]);

  useEffect(() => {
    loadDocuments();
  }, [caseId]);

  const loadDocuments = async () => {
    try {
      const response = await api.get(`/cases/${caseId}/documents`);
      setDocuments(response.data);
    } catch (error) {
      console.error("Failed to load docs:", error);
    }
  };

  const handleFileUpload = async (event, docType) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await api.post(`/cases/${caseId}/documents/analyze?doc_type=${docType}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      toast.success(`${docType} uploaded & analyzed`);
      await loadDocuments();
    } catch (error) {
      toast.error("Upload failed");
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  const toggleDocSelection = (docId) => {
    if (selectedDocs.includes(docId)) {
      setSelectedDocs(selectedDocs.filter(id => id !== docId));
    } else {
      if (selectedDocs.length < 2) {
        setSelectedDocs([...selectedDocs, docId]);
      } else {
        toast.info("Select exactly 2 documents to compare");
      }
    }
  };

  const runComparison = async () => {
    if (selectedDocs.length !== 2) return;
    
    setComparing(true);
    setComparisonResult(null);
    try {
      const response = await api.post(`/cases/${caseId}/documents/compare`, null, {
        params: { doc1_id: selectedDocs[0], doc2_id: selectedDocs[1] }
      });
      setComparisonResult(response.data);
      if (response.data.match === false) {
        toast.error("Discrepancies found!", { duration: 4000 });
      } else {
        toast.success("Documents match!", { duration: 4000 });
      }
    } catch (error) {
      toast.error("Comparison failed");
    } finally {
      setComparing(false);
    }
  };

  return (
    <Card>
      <CardHeader className="pb-3 border-b">
        <div className="flex justify-between items-center">
          <CardTitle className="text-base flex items-center gap-2">
            <div className="p-1.5 bg-gray-100 rounded-md">
              <FileText className="h-4 w-4 text-gray-700" />
            </div>
            Document Intelligence
          </CardTitle>
          <div className="flex gap-2">
            <div className="relative">
              <input
                type="file"
                id="upload-invoice"
                className="hidden"
                onChange={(e) => handleFileUpload(e, "Invoice")}
                accept=".pdf,.jpg,.png"
              />
              <Button variant="outline" size="sm" asChild disabled={uploading} className="h-8 text-xs">
                <label htmlFor="upload-invoice" className="cursor-pointer">
                  {uploading ? <Loader2 className="h-3 w-3 animate-spin mr-1" /> : <Upload className="h-3 w-3 mr-1" />}
                  Invoice
                </label>
              </Button>
            </div>
            <div className="relative">
              <input
                type="file"
                id="upload-bl"
                className="hidden"
                onChange={(e) => handleFileUpload(e, "Bill of Lading")}
                accept=".pdf,.jpg,.png"
              />
              <Button variant="outline" size="sm" asChild disabled={uploading} className="h-8 text-xs">
                <label htmlFor="upload-bl" className="cursor-pointer">
                  {uploading ? <Loader2 className="h-3 w-3 animate-spin mr-1" /> : <Upload className="h-3 w-3 mr-1" />}
                  Bill of Lading
                </label>
              </Button>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-4">
        {documents.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground text-sm border-2 border-dashed rounded-lg bg-gray-50/50">
            <FileText className="h-8 w-8 mx-auto text-gray-300 mb-2" />
            <p>No documents uploaded.</p>
            <p className="text-xs mt-1">Upload an Invoice and BL to check for mismatches.</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-2">
              {documents.map((doc) => {
                const isSelected = selectedDocs.includes(doc._id);
                return (
                  <div 
                    key={doc._id} 
                    className={`p-3 rounded-lg border flex justify-between items-center cursor-pointer transition-all duration-200 ${
                      isSelected 
                        ? "border-blue-500 bg-blue-50/50 shadow-sm" 
                        : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                    }`}
                    onClick={() => toggleDocSelection(doc._id)}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${
                        isSelected ? "bg-blue-500 border-blue-500" : "border-gray-300 bg-white"
                      }`}>
                        {isSelected && <CheckCircle2 className="w-3 h-3 text-white" />}
                      </div>
                      <div>
                        <p className="font-medium text-sm text-gray-900">{doc.filename}</p>
                        <div className="flex items-center gap-2 mt-0.5">
                          <Badge variant="outline" className="text-[10px] font-normal px-1.5 h-4 bg-white">
                            {doc.doc_type}
                          </Badge>
                          <span className="text-xs text-gray-400">
                            {new Date(doc.uploaded_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                          </span>
                        </div>
                      </div>
                    </div>
                    {doc.analysis ? (
                      <div className="flex items-center text-xs text-green-600 font-medium">
                        <CheckCircle2 className="h-3 w-3 mr-1" /> Analyzed
                      </div>
                    ) : (
                      <Badge variant="secondary" className="text-xs">Pending</Badge>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Comparison Controls */}
            {selectedDocs.length === 2 && (
              <div className="flex justify-end pt-2 animate-in fade-in slide-in-from-bottom-1">
                <Button onClick={runComparison} disabled={comparing} size="sm" className="bg-slate-800 text-white hover:bg-slate-700">
                  {comparing ? <Loader2 className="h-3 w-3 animate-spin mr-2" /> : <GitCompare className="h-3 w-3 mr-2" />}
                  Compare Selected Docs
                </Button>
              </div>
            )}

            {/* Comparison Results */}
            {comparisonResult && (
              <div className={`mt-4 p-4 rounded-lg border shadow-sm animate-in zoom-in-95 duration-300 ${
                comparisonResult.match ? "bg-green-50/50 border-green-200" : "bg-red-50/50 border-red-200"
              }`}>
                <div className="flex items-start gap-3">
                  <div className={`p-2 rounded-full ${comparisonResult.match ? "bg-green-100" : "bg-red-100"}`}>
                    {comparisonResult.match ? (
                      <CheckCircle2 className="h-5 w-5 text-green-600" />
                    ) : (
                      <AlertTriangle className="h-5 w-5 text-red-600" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h4 className={`font-semibold ${comparisonResult.match ? "text-green-900" : "text-red-900"}`}>
                      {comparisonResult.match ? "Documents Match" : "Discrepancy Detected"}
                    </h4>
                    <p className={`text-sm mt-1 ${comparisonResult.match ? "text-green-700" : "text-red-700"}`}>
                      {comparisonResult.summary}
                    </p>
                    
                    {comparisonResult.discrepancies?.length > 0 && (
                      <div className="mt-3 space-y-2">
                        {comparisonResult.discrepancies.map((disc, idx) => (
                          <div key={idx} className="bg-white p-2.5 rounded border border-red-100 text-sm shadow-sm">
                            <div className="flex justify-between mb-1.5">
                              <span className="font-medium text-red-800 text-xs uppercase tracking-wide">{disc.field}</span>
                              <Badge variant="outline" className="text-[10px] border-red-200 text-red-600">High Severity</Badge>
                            </div>
                            <div className="grid grid-cols-2 gap-4 text-xs">
                              <div>
                                <span className="text-gray-500 block mb-0.5">Doc 1 Value</span>
                                <span className="font-mono bg-red-50 px-1.5 py-0.5 rounded text-red-700 block truncate" title={disc.doc1_value}>
                                  {disc.doc1_value}
                                </span>
                              </div>
                              <div>
                                <span className="text-gray-500 block mb-0.5">Doc 2 Value</span>
                                <span className="font-mono bg-green-50 px-1.5 py-0.5 rounded text-green-700 block truncate" title={disc.doc2_value}>
                                  {disc.doc2_value}
                                </span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default DocumentManager;
