<template>
  <div class="bg-white rounded-lg shadow-md p-6 mb-6">
    <h3 class="text-lg font-semibold mb-4">Financial Analysis Results</h3>
    
    <div v-if="loading" class="text-center py-4">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-2 text-gray-600">Analyzing financial data...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
      <p class="text-red-700">{{ error }}</p>
    </div>
    
    <div v-else-if="analysis" class="space-y-4">
      <!-- Analysis Summary -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-blue-50 p-4 rounded-lg">
          <h4 class="font-medium text-blue-800">Articles Analyzed</h4>
          <p class="text-2xl font-bold text-blue-600">{{ analysis.news_summary?.total_articles || 0 }}</p>
        </div>
        <div class="bg-green-50 p-4 rounded-lg">
          <h4 class="font-medium text-green-800">Market Outlook</h4>
          <p class="text-lg font-semibold capitalize text-green-600">{{ analysis.market_outlook?.sentiment || 'neutral' }}</p>
        </div>
        <div class="bg-purple-50 p-4 rounded-lg">
          <h4 class="font-medium text-purple-800">Confidence</h4>
          <p class="text-lg font-semibold text-purple-600">{{ analysis.market_outlook?.confidence || 0 }}%</p>
        </div>
      </div>
      
      <!-- Key Insights -->
      <div v-if="analysis.key_insights?.length" class="bg-yellow-50 p-4 rounded-lg">
        <h4 class="font-medium text-yellow-800 mb-2">Key Insights</h4>
        <ul class="list-disc list-inside space-y-1">
          <li v-for="insight in analysis.key_insights" :key="insight" class="text-yellow-700">
            {{ insight }}
          </li>
        </ul>
      </div>
      
      <!-- Investment Recommendations -->
      <div v-if="analysis.investment_recommendations?.length" class="bg-green-50 p-4 rounded-lg">
        <h4 class="font-medium text-green-800 mb-2">Investment Recommendations</h4>
        <div class="space-y-2">
          <div v-for="rec in analysis.investment_recommendations" :key="rec.action" 
               class="border-l-4 border-green-500 pl-3">
            <p class="font-medium text-green-700">{{ rec.action }}</p>
            <p class="text-sm text-green-600">{{ rec.rationale }}</p>
            <span class="inline-block px-2 py-1 text-xs rounded-full" 
                  :class="{
                    'bg-red-100 text-red-800': rec.priority === 'High',
                    'bg-yellow-100 text-yellow-800': rec.priority === 'Medium',
                    'bg-green-100 text-green-800': rec.priority === 'Low'
                  }">
              {{ rec.priority }} Priority
            </span>
          </div>
        </div>
      </div>
      
      <!-- Risk Assessment -->
      <div v-if="analysis.risk_assessment?.length" class="bg-red-50 p-4 rounded-lg">
        <h4 class="font-medium text-red-800 mb-2">Risk Assessment</h4>
        <ul class="list-disc list-inside space-y-1">
          <li v-for="risk in analysis.risk_assessment" :key="risk" class="text-red-700">
            {{ risk }}
          </li>
        </ul>
      </div>
      
      <!-- Opportunities -->
      <div v-if="analysis.opportunities?.length" class="bg-blue-50 p-4 rounded-lg">
        <h4 class="font-medium text-blue-800 mb-2">Opportunities</h4>
        <ul class="list-disc list-inside space-y-1">
          <li v-for="opportunity in analysis.opportunities" :key="opportunity" class="text-blue-700">
            {{ opportunity }}
          </li>
        </ul>
      </div>
      
      <!-- News Articles -->
      <div v-if="analysis.news_summary?.articles?.length" class="border-t pt-4">
        <h4 class="font-medium text-gray-800 mb-3">Recent News Articles</h4>
        <div class="space-y-3">
          <div v-for="article in analysis.news_summary.articles" :key="article.url" 
               class="border rounded-lg p-3 hover:bg-gray-50">
            <a :href="article.url" target="_blank" class="text-blue-600 hover:text-blue-800 font-medium">
              {{ article.title }}
            </a>
            <p class="text-sm text-gray-600 mt-1">{{ article.summary }}</p>
            <p class="text-xs text-gray-500 mt-2">Published: {{ article.published_date }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getFinancialAnalysis } from '../services/api.js'

export default {
  name: 'FinancialAnalysisCard',
  props: {
    companyName: String,
    industry: String,
    product: String,
    exaKey: String
  },
  data() {
    return {
      loading: false,
      error: null,
      analysis: null
    }
  },
  watch: {
    companyName: {
      handler: 'fetchAnalysis',
      immediate: true
    },
    industry: {
      handler: 'fetchAnalysis',
      immediate: true
    },
    product: {
      handler: 'fetchAnalysis',
      immediate: true
    }
  },
  methods: {
    async fetchAnalysis() {
      if (!this.exaKey || (!this.companyName && !this.industry && !this.product)) {
        this.analysis = null
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        const params = {
          company_name: this.companyName,
          industry: this.industry,
          product: this.product,
          max_results: 10
        }
        
        this.analysis = await getFinancialAnalysis(params, this.exaKey)
      } catch (error) {
        this.error = error.response?.data?.error || error.message || 'Failed to fetch financial analysis'
        console.error('Financial analysis error:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Component-specific styles */
</style>