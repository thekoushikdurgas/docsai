// GraphQL Client for Django DocsAI App

class GraphQLClient {
    constructor(endpoint, apiKey) {
        this.endpoint = endpoint || '/graphql';
        this.apiKey = apiKey || '';
    }

    async executeQuery(query, variables = {}) {
        try {
            const response = await fetch(this.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    ...(this.apiKey && { 'Authorization': `Bearer ${this.apiKey}` })
                },
                body: JSON.stringify({
                    query,
                    variables
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            if (!result || typeof result !== 'object') {
                throw new Error('GraphQL: invalid JSON response');
            }

            if (result.errors && Array.isArray(result.errors) && result.errors.length) {
                const msg = result.errors.map(function (e) {
                    return (e && e.message) ? e.message : String(e);
                }).join(', ');
                throw new Error(msg || 'GraphQL errors');
            }

            if (!Object.prototype.hasOwnProperty.call(result, 'data')) {
                throw new Error('GraphQL: response missing data field');
            }

            return result.data;
        } catch (error) {
            console.error('GraphQL query error:', error);
            throw error;
        }
    }

    async executeMutation(mutation, variables = {}) {
        return this.executeQuery(mutation, variables);
    }
}

// Initialize global GraphQL client
window.graphql = new GraphQLClient(
    window.GRAPHQL_ENDPOINT || 'http://api.contact360.io/graphql',
    window.GRAPHQL_API_KEY || ''
);
