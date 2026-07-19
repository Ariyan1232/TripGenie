import client from './client';

export const createTrip = async (data) => {
  const response = await client.post('/trips', data);
  return response.data;
};

export const getTrip = async (tripId) => {
  const response = await client.get(`/trips/${tripId}`);
  return response.data;
};

export const addTraveler = async (tripId, data) => {
  const response = await client.post(`/trips/${tripId}/travelers`, data);
  return response.data;
};

export const getResults = async (tripId) => {
  const response = await client.get(`/trips/${tripId}/results`);
  return response.data;
};