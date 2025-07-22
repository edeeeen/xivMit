/***************************************
 *     API fetching script             *
 ***************************************/

import axios from 'axios';

// Create an instance of axios with the base URL

// Make it read from env this is stupid
const api = axios.create({
  baseURL: "https://xivmit-backend-a3a8ebhaczh2dqar.eastus-01.azurewebsites.net/api"
});

// Export the Axios instance
export default api;