import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, FileText, Upload, AlertTriangle, CheckCircle2, GitCompare } from "lucide-react";
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
        toast.error("Discrepancies found!");
      } else {
        toast.success("Documents match!");
      }
    } catch (error) {
      toast.error("Comparison failed");
    } finally {
      setComparing(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="pb-2">
          <div className="flex justify-between items-center">
            <CardTitle className="text-lg flex items-center gap-2">
              <FileText className="h-5 w-5" />
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
                <Button variant="outline" size="sm" asChild disabled={uploading}>
                  <label htmlFor="upload-invoice" className="cursor-pointer">
                    {uploading ? <Loader2 className="h-3 w-3 animate-spin" /> : <Upload className="h-3 w-3 mr-2" />}
                    Upload Invoice
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
                <Button variant="outline" size="sm" asChild disabled={uploading}>
                  <label htmlFor="upload-bl" className="cursor-pointer">
                    {uploading ? <Loader2 className="h-3 w-3 animate-spin" /> : <Upload className="h-3 w-3 mr-2" />}
                    Upload BL
                  </label>
                </Button>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {documents.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground text-sm border-2 border-dashed rounded-lg">
              No documents uploaded. Upload an Invoice and BL to check for mismatches.
            </div>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-1 gap-2">
                {documents.map((doc) => (
                  <div 
                    key={doc._id} 
                    className={`p-3 rounded-lg border flex justify-between items-center cursor-pointer transition-colors ${
                      selectedDocs.includes(doc._id) ? "border-blue-500 bg-blue-50" : "hover:bg-gray-50"
                    }`}
                    onClick={() => toggleDocSelection(doc._id)}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-4 h-4 rounded border ${selectedDocs.includes(doc._id) ? "bg-blue-500 border-blue-500" : "border-gray-300"}`}>
                        {selectedDocs.includes(doc._id) && <CheckCircle2 className="w-4 h-4 text-white" />}
                      </div>
                      <div>
                        <p className="font-medium text-sm">{doc.filename}</p>
                        <p className="text-xs text-muted-foreground">{doc.doc_type} • Uploaded {new Date(doc.uploaded_at).toLocaleTimeString()}</p>
                      </div>
                    </div>
                    <Badge variant="secondary" className="text-xs">
                      {doc.analysis ? "Analyzed" : "Pending"}
                    </Badge>
                  </div>
                ))}
              </div>

              {selectedDocs.length === 2 && (
                <div className="flex justify-end">
                  <Button onClick={runComparison} disabled={comparing}>
                    {comparing ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <GitCompare className="h-4 w-4 mr-2" />}
                    Compare Selected Documents
                  </Button>
                </div>
              )}

              {comparisonResult && (
                <div className={`mt-4 p-4 rounded-lg border ${comparisonResult.match ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"}`}>
                  <div className="flex items-start gap-3">
                    {comparisonResult.match ? (
                      <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5" />
                    ) : (
                      <AlertTriangle className="h-5 w-5 text-red-600 mt-0.5" />
                    )}
                    <div>
                      <h4 className={`font-medium ${comparisonResult.match ? "text-green-900" : "text-red-900"}`}>
                        {comparisonResult.match ? "Documents Match" : "Discrepancy Detected"}
                      </h4>
                      <p className={`text-sm mt-1 ${comparisonResult.match ? "text-green-700" : "text-red-700"}`}>
                        {comparisonResult.summary}
                      </p>
                      
                      {comparisonResult.discrepancies?.length > 0 && (
                        <div className="mt-3 space-y-2">
                          {comparisonResult.discrepancies.map((disc, idx) => (
                            <div key={idx} className="bg-white/50 p-2 rounded text-sm border border-red-100">
                              <span className="font-medium block text-red-800">{disc.field}</span>
                              <div className="grid grid-cols-2 gap-2 mt-1 text-xs">
                                <div>Doc 1: <span className="font-mono bg-red-100 px-1 rounded">{disc.doc1_value}</span></div>
                                <div>Doc 2: <span className="font-mono bg-green-100 px-1 rounded">{disc.doc2_value}</span></div>
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
    </div>
  );
};

export default DocumentManager;
