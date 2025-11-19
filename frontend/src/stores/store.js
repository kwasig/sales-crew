import { reactive } from 'vue'

export const store = reactive({
  backendUrl: 'http://localhost:8000',
  apiKey: null,
  searchResults: [],
  loading: false,
  error: null
})

export function useStore() {
  return {
    store
  }
}