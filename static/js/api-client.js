// API Client for Django REST endpoints

class APIClient {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const timeoutMs = options.timeoutMs !== undefined ? options.timeoutMs : 60000;
        const signal = options.signal;

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            },
        };

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers,
            }
        };

        delete mergedOptions.timeoutMs;

        let controller = null;
        let timeoutId = null;
        if (timeoutMs > 0 && !signal) {
            controller = new AbortController();
            mergedOptions.signal = controller.signal;
            timeoutId = setTimeout(function () {
                controller.abort();
            }, timeoutMs);
        }

        if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
            mergedOptions.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, mergedOptions);
            if (timeoutId) clearTimeout(timeoutId);
            const contentType = response.headers.get('content-type') || '';
            if (contentType.includes('application/json')) {
                return await response.json();
            }
            const text = await response.text();
            try {
                return JSON.parse(text);
            } catch (e) {
                return { raw: text, ok: response.ok, status: response.status };
            }
        } catch (error) {
            if (timeoutId) clearTimeout(timeoutId);
            throw error;
        }
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, { method: 'POST', body: data });
    }

    async put(endpoint, data) {
        return this.request(endpoint, { method: 'PUT', body: data });
    }

    async patch(endpoint, data) {
        return this.request(endpoint, { method: 'PATCH', body: data });
    }

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Initialize global API client
window.api = new APIClient();
