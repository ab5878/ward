/**
 * API v0 Service
 * Service layer for API v0 endpoints (Movements, Events, Attachments, DisputePackets, Facilities, Parties)
 */

import api from './api';

// ============================================================================
// Movements API
// ============================================================================

export const movementsAPI = {
  /**
   * Create or upsert a movement
   * @param {Object} movementData - Movement data
   * @returns {Promise} Movement object
   */
  create: async (movementData) => {
    const response = await api.post('/v0/movements', movementData);
    return response.data;
  },

  /**
   * List movements with filters
   * @param {Object} filters - Filter options (container_id, truck_id, external_id, status, limit, offset)
   * @returns {Promise} Object with items, total, limit, offset
   */
  list: async (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, value);
      }
    });
    const response = await api.get(`/v0/movements?${params.toString()}`);
    return response.data;
  },

  /**
   * Get a movement by ID
   * @param {string} movementId - Movement ID
   * @returns {Promise} Movement object
   */
  get: async (movementId) => {
    const response = await api.get(`/v0/movements/${movementId}`);
    return response.data;
  },
};

// ============================================================================
// Events API
// ============================================================================

export const eventsAPI = {
  /**
   * Create an event for a movement
   * @param {Object} eventData - Event data (movement_id, event_type, location, device_id, content, etc.)
   * @returns {Promise} Event object
   */
  create: async (eventData) => {
    const response = await api.post('/v0/events', eventData);
    return response.data;
  },
};

// ============================================================================
// Attachments API
// ============================================================================

export const attachmentsAPI = {
  /**
   * Upload an attachment
   * @param {File} file - File to upload
   * @param {Object} options - Options (event_id, movement_id, file_type, description)
   * @returns {Promise} Attachment object
   */
  upload: async (file, options = {}) => {
    const formData = new FormData();
    formData.append('file', file);
    
    if (options.event_id) formData.append('event_id', options.event_id);
    if (options.movement_id) formData.append('movement_id', options.movement_id);
    if (options.file_type) formData.append('file_type', options.file_type);
    if (options.description) formData.append('description', options.description);

    const response = await api.post('/v0/attachments', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  /**
   * Get an attachment by ID
   * @param {string} attachmentId - Attachment ID
   * @returns {Promise} Attachment object
   */
  get: async (attachmentId) => {
    const response = await api.get(`/v0/attachments/${attachmentId}`);
    return response.data;
  },

  /**
   * List attachments for an event
   * @param {string} eventId - Event ID
   * @returns {Promise} Array of attachment objects
   */
  listForEvent: async (eventId) => {
    const response = await api.get(`/v0/events/${eventId}/attachments`);
    return response.data;
  },
};

// ============================================================================
// DisputePackets API
// ============================================================================

export const disputePacketsAPI = {
  /**
   * Create a dispute packet for a movement
   * @param {string} movementId - Movement ID
   * @param {Object} packetData - Packet data (invoice_id, template_type, selected_events, narrative, etc.)
   * @returns {Promise} DisputePacket object
   */
  create: async (movementId, packetData) => {
    const response = await api.post(`/v0/movements/${movementId}/dispute-packets`, packetData);
    return response.data;
  },

  /**
   * List dispute packets for a movement
   * @param {string} movementId - Movement ID
   * @returns {Promise} Array of dispute packet objects
   */
  list: async (movementId) => {
    const response = await api.get(`/v0/movements/${movementId}/dispute-packets`);
    return response.data;
  },

  /**
   * Get a dispute packet by ID
   * @param {string} packetId - DisputePacket ID
   * @returns {Promise} DisputePacket object
   */
  get: async (packetId) => {
    const response = await api.get(`/v0/dispute-packets/${packetId}`);
    return response.data;
  },

  /**
   * Export dispute packet as ZIP
   * @param {string} packetId - DisputePacket ID
   * @returns {Promise} Blob of ZIP file
   */
  export: async (packetId) => {
    const response = await api.post(`/v0/dispute-packets/${packetId}/export`, {}, {
      responseType: 'blob'
    });
    return response.data;
  },

  /**
   * Update a dispute packet
   * @param {string} packetId - DisputePacket ID
   * @param {Object} updateData - Update data (status, narrative, outcome, outcome_amount, etc.)
   * @returns {Promise} Updated DisputePacket object
   */
  update: async (packetId, updateData) => {
    const response = await api.patch(`/v0/dispute-packets/${packetId}`, updateData);
    return response.data;
  },
};

// ============================================================================
// Facilities API
// ============================================================================

export const facilitiesAPI = {
  /**
   * Create a facility
   * @param {Object} facilityData - Facility data (name, type, code, address, location, etc.)
   * @returns {Promise} Facility object
   */
  create: async (facilityData) => {
    const response = await api.post('/v0/facilities', facilityData);
    return response.data;
  },

  /**
   * List facilities with optional type filter
   * @param {Object} filters - Filter options (type)
   * @returns {Promise} Array of facility objects
   */
  list: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.type) params.append('type', filters.type);
    const response = await api.get(`/v0/facilities?${params.toString()}`);
    return response.data;
  },

  /**
   * Get a facility by ID
   * @param {string} facilityId - Facility ID
   * @returns {Promise} Facility object
   */
  get: async (facilityId) => {
    const response = await api.get(`/v0/facilities/${facilityId}`);
    return response.data;
  },
};

// ============================================================================
// Parties API
// ============================================================================

export const partiesAPI = {
  /**
   * Create a party
   * @param {Object} partyData - Party data (name, type, code, contact_info, etc.)
   * @returns {Promise} Party object
   */
  create: async (partyData) => {
    const response = await api.post('/v0/parties', partyData);
    return response.data;
  },

  /**
   * List parties with optional type filter
   * @param {Object} filters - Filter options (type)
   * @returns {Promise} Array of party objects
   */
  list: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.type) params.append('type', filters.type);
    const response = await api.get(`/v0/parties?${params.toString()}`);
    return response.data;
  },

  /**
   * Get a party by ID
   * @param {string} partyId - Party ID
   * @returns {Promise} Party object
   */
  get: async (partyId) => {
    const response = await api.get(`/v0/parties/${partyId}`);
    return response.data;
  },
};

// ============================================================================
// Default Export
// ============================================================================

export default {
  movements: movementsAPI,
  events: eventsAPI,
  attachments: attachmentsAPI,
  disputePackets: disputePacketsAPI,
  facilities: facilitiesAPI,
  parties: partiesAPI,
};

