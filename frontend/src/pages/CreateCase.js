import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Plus, X } from 'lucide-react';

export default function CreateCase() {
  const [description, setDescription] = useState('');
  
  // Disruption Details (REQUIRED)
  const [disruptionType, setDisruptionType] = useState('');
  const [scope, setScope] = useState('');
  const [identifier, setIdentifier] = useState('');
  const [timeDiscoveredIST, setTimeDiscoveredIST] = useState('');
  const [source, setSource] = useState('');
  
  const [shipmentIds, setShipmentIds] = useState(['']);
  const [routes, setRoutes] = useState(['']);
  const [carriers, setCarriers] = useState(['']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const addField = (setter, arr) => {
    setter([...arr, '']);
  };

  const removeField = (setter, arr, index) => {
    setter(arr.filter((_, i) => i !== index));
  };

  const updateField = (setter, arr, index, value) => {
    const updated = [...arr];
    updated[index] = value;
    setter(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post('/cases', {
        description,
        disruption_details: {
          disruption_type: disruptionType,
          scope: scope,
          identifier: identifier,
          time_discovered_ist: timeDiscoveredIST,
          source: source,
        },
        shipment_identifiers: {
          ids: shipmentIds.filter(id => id.trim()),
          routes: routes.filter(r => r.trim()),
          carriers: carriers.filter(c => c.trim()),
        },
      });

      navigate(`/cases/${response.data._id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create case');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-[hsl(var(--border))] bg-card">
        <div className="container mx-auto px-6 py-4">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 text-sm text-[hsl(var(--muted-foreground))] hover:text-foreground transition-colors mb-2"
            data-testid="back-to-dashboard"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
          <h1 className="text-2xl font-bold">New Disruption Case</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))]">
            Describe the live disruption requiring a decision
          </p>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8 max-w-3xl">
        <form onSubmit={handleSubmit} className="bg-card border border-[hsl(var(--border))] rounded-lg p-6">
          {error && (
            <div className="mb-4 p-3 rounded-md bg-[hsl(var(--destructive))]/10 border border-[hsl(var(--destructive))]/20 text-sm text-[hsl(var(--destructive))]">
              {error}
            </div>
          )}

          {/* Description */}
          <div className="mb-6">
            <label htmlFor="description" className="block text-sm font-medium mb-2">
              Disruption Description *
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              minLength={10}
              rows={6}
              className="w-full px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background resize-none"
              placeholder="Describe the disruption: what happened, when, current status, time constraints..."
              data-testid="description-input"
            />
            <p className="mt-1 text-xs text-[hsl(var(--muted-foreground))]">
              Be specific: include timing, scope, and urgency
            </p>
          </div>

          {/* Shipment IDs */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Shipment IDs</label>
            {shipmentIds.map((id, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={id}
                  onChange={(e) => updateField(setShipmentIds, shipmentIds, index, e.target.value)}
                  className="flex-1 px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background"
                  placeholder="SH-2024-XXX"
                  data-testid={`shipment-id-${index}`}
                />
                {shipmentIds.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField(setShipmentIds, shipmentIds, index)}
                    className="p-2 text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--destructive))] transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField(setShipmentIds, shipmentIds)}
              className="flex items-center gap-1 text-sm text-[hsl(var(--primary))] hover:underline"
              data-testid="add-shipment-id"
            >
              <Plus className="h-3 w-3" />
              Add Shipment ID
            </button>
          </div>

          {/* Routes */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Routes</label>
            {routes.map((route, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={route}
                  onChange={(e) => updateField(setRoutes, routes, index, e.target.value)}
                  className="flex-1 px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background"
                  placeholder="New York → Chicago → Denver"
                  data-testid={`route-${index}`}
                />
                {routes.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField(setRoutes, routes, index)}
                    className="p-2 text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--destructive))] transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField(setRoutes, routes)}
              className="flex items-center gap-1 text-sm text-[hsl(var(--primary))] hover:underline"
              data-testid="add-route"
            >
              <Plus className="h-3 w-3" />
              Add Route
            </button>
          </div>

          {/* Carriers */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Carriers</label>
            {carriers.map((carrier, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={carrier}
                  onChange={(e) => updateField(setCarriers, carriers, index, e.target.value)}
                  className="flex-1 px-3 py-2 border border-[hsl(var(--input))] rounded-md focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] bg-background"
                  placeholder="FastFreight Express"
                  data-testid={`carrier-${index}`}
                />
                {carriers.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeField(setCarriers, carriers, index)}
                    className="p-2 text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--destructive))] transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>
            ))}
            <button
              type="button"
              onClick={() => addField(setCarriers, carriers)}
              className="flex items-center gap-1 text-sm text-[hsl(var(--primary))] hover:underline"
              data-testid="add-carrier"
            >
              <Plus className="h-3 w-3" />
              Add Carrier
            </button>
          </div>

          {/* Actions */}
          <div className="flex gap-3 justify-end pt-4 border-t border-[hsl(var(--border))]">
            <Link
              to="/dashboard"
              className="px-4 py-2 text-sm border border-[hsl(var(--border))] rounded-md hover:bg-[hsl(var(--secondary))] transition-colors"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors disabled:opacity-50"
              data-testid="submit-case-button"
            >
              {loading ? 'Creating...' : 'Create Case'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
