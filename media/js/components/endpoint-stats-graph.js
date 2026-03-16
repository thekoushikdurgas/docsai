/**
 * EndpointStatsGraph - D3.js visualization for endpoint usage by user type
 * 
 * Displays API endpoint statistics broken down by user type with multiple view options:
 * - Grouped Bar Chart: Side-by-side bars for each user type
 * - Stacked Bar Chart: Stacked bars showing proportions
 * - Heatmap: Color-coded matrix view
 * 
 * Requires: D3.js v7+
 */

class EndpointStatsGraph {
    constructor(containerId, data, options = {}) {
        this.containerId = containerId;
        this.container = d3.select(`#${containerId}`);
        this.data = data;
        this.options = {
            view: options.view || 'grouped',  // 'grouped', 'stacked', 'heatmap'
            width: options.width || null,  // null = auto (responsive)
            height: options.height || 400,
            margin: options.margin || { top: 20, right: 120, bottom: 80, left: 60 },
            showLegend: options.showLegend !== false,
            sortBy: options.sortBy || 'total',  // 'total', 'name', specific user_type
            topN: options.topN || null,  // Show only top N endpoints
            ...options
        };
        
        // User types and colors
        this.userTypes = ['super_admin', 'admin', 'pro_user', 'free_user', 'guest'];
        this.colors = {
            super_admin: '#dc2626',  // red-600
            admin: '#ea580c',        // orange-600
            pro_user: '#2563eb',     // blue-600
            free_user: '#059669',    // green-600
            guest: '#6b7280'         // gray-500
        };
        
        this.userTypeLabels = {
            super_admin: 'Super Admin',
            admin: 'Admin',
            pro_user: 'Pro User',
            free_user: 'Free User',
            guest: 'Guest'
        };
        
        // State
        this.hiddenUserTypes = new Set();
        this.svg = null;
        this.tooltip = null;
        
        this._init();
    }
    
    _init() {
        // Clear container
        this.container.selectAll('*').remove();
        
        // Create tooltip
        this.tooltip = d3.select('body').append('div')
            .attr('class', 'endpoint-graph-tooltip')
            .style('position', 'absolute')
            .style('visibility', 'hidden')
            .style('background', 'rgba(0, 0, 0, 0.9)')
            .style('color', 'white')
            .style('padding', '8px 12px')
            .style('border-radius', '6px')
            .style('font-size', '12px')
            .style('pointer-events', 'none')
            .style('z-index', '1000')
            .style('box-shadow', '0 2px 8px rgba(0,0,0,0.2)');
    }
    
    render() {
        // Process data
        const processedData = this._processData();
        
        if (!processedData || processedData.length === 0) {
            this._renderEmptyState();
            return;
        }
        
        // Render based on view type
        switch (this.options.view) {
            case 'stacked':
                this._renderStackedBarChart(processedData);
                break;
            case 'heatmap':
                this._renderHeatmap(processedData);
                break;
            case 'grouped':
            default:
                this._renderGroupedBarChart(processedData);
                break;
        }
        
        // Render legend if enabled
        if (this.options.showLegend) {
            this._renderLegend();
        }
    }
    
    _processData() {
        if (!this.data || !this.data.by_endpoint) {
            console.warn('No data available for graph');
            return [];
        }
        
        const byEndpoint = this.data.by_endpoint;
        let endpoints = [];
        
        // Convert to array format
        for (const [endpointKey, userTypeStats] of Object.entries(byEndpoint)) {
            const endpoint = { name: endpointKey, total: 0 };
            
            for (const userType of this.userTypes) {
                const count = userTypeStats[userType]?.request_count || 0;
                endpoint[userType] = count;
                endpoint.total += count;
            }
            
            endpoints.push(endpoint);
        }
        
        // Sort
        if (this.options.sortBy === 'total') {
            endpoints.sort((a, b) => b.total - a.total);
        } else if (this.options.sortBy === 'name') {
            endpoints.sort((a, b) => a.name.localeCompare(b.name));
        } else if (this.userTypes.includes(this.options.sortBy)) {
            endpoints.sort((a, b) => (b[this.options.sortBy] || 0) - (a[this.options.sortBy] || 0));
        }
        
        // Limit to top N
        if (this.options.topN) {
            endpoints = endpoints.slice(0, this.options.topN);
        }
        
        return endpoints;
    }
    
    _renderGroupedBarChart(data) {
        const container = this.container.node();
        const containerWidth = this.options.width || container.clientWidth;
        const { margin, height } = this.options;
        const width = containerWidth - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        // Clear and create SVG
        this.container.selectAll('*').remove();
        this.svg = this.container.append('svg')
            .attr('width', containerWidth)
            .attr('height', height)
            .attr('class', 'endpoint-stats-graph');
        
        const g = this.svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        // Scales
        const x0 = d3.scaleBand()
            .domain(data.map(d => d.name))
            .rangeRound([0, width])
            .paddingInner(0.1);
        
        const x1 = d3.scaleBand()
            .domain(this.userTypes.filter(ut => !this.hiddenUserTypes.has(ut)))
            .rangeRound([0, x0.bandwidth()])
            .padding(0.05);
        
        const maxValue = d3.max(data, d => d3.max(this.userTypes, ut => d[ut] || 0));
        const y = d3.scaleLinear()
            .domain([0, maxValue])
            .nice()
            .rangeRound([innerHeight, 0]);
        
        // Axes
        const xAxis = g.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0,${innerHeight})`)
            .call(d3.axisBottom(x0))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end')
            .style('font-size', '10px');
        
        g.append('g')
            .attr('class', 'y-axis')
            .call(d3.axisLeft(y).ticks(10))
            .append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', -40)
            .attr('dy', '0.71em')
            .attr('text-anchor', 'end')
            .attr('fill', 'currentColor')
            .style('font-size', '12px')
            .text('Requests');
        
        // Bars
        const endpoint = g.selectAll('.endpoint')
            .data(data)
            .enter().append('g')
            .attr('class', 'endpoint')
            .attr('transform', d => `translate(${x0(d.name)},0)`);
        
        endpoint.selectAll('rect')
            .data(d => this.userTypes
                .filter(ut => !this.hiddenUserTypes.has(ut))
                .map(ut => ({ key: ut, value: d[ut] || 0, endpoint: d.name })))
            .enter().append('rect')
            .attr('x', d => x1(d.key))
            .attr('y', d => y(d.value))
            .attr('width', x1.bandwidth())
            .attr('height', d => innerHeight - y(d.value))
            .attr('fill', d => this.colors[d.key])
            .attr('opacity', 0.85)
            .on('mouseover', (event, d) => this._showTooltip(event, d))
            .on('mouseout', () => this._hideTooltip())
            .on('click', (event, d) => this._onBarClick(d));
        
        // Dark mode support
        this._applyDarkModeStyles(g);
    }
    
    _renderStackedBarChart(data) {
        const container = this.container.node();
        const containerWidth = this.options.width || container.clientWidth;
        const { margin, height } = this.options;
        const width = containerWidth - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        // Clear and create SVG
        this.container.selectAll('*').remove();
        this.svg = this.container.append('svg')
            .attr('width', containerWidth)
            .attr('height', height);
        
        const g = this.svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        // Stack data
        const visibleUserTypes = this.userTypes.filter(ut => !this.hiddenUserTypes.has(ut));
        const stack = d3.stack()
            .keys(visibleUserTypes)
            .value((d, key) => d[key] || 0);
        
        const series = stack(data);
        
        // Scales
        const x = d3.scaleBand()
            .domain(data.map(d => d.name))
            .range([0, width])
            .padding(0.1);
        
        const y = d3.scaleLinear()
            .domain([0, d3.max(series, s => d3.max(s, d => d[1]))])
            .nice()
            .range([innerHeight, 0]);
        
        // Axes
        g.append('g')
            .attr('transform', `translate(0,${innerHeight})`)
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end')
            .style('font-size', '10px');
        
        g.append('g')
            .call(d3.axisLeft(y).ticks(10))
            .append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', -40)
            .attr('dy', '0.71em')
            .attr('text-anchor', 'end')
            .attr('fill', 'currentColor')
            .text('Requests');
        
        // Bars
        g.selectAll('.layer')
            .data(series)
            .enter().append('g')
            .attr('class', 'layer')
            .attr('fill', d => this.colors[d.key])
            .attr('opacity', 0.85)
            .selectAll('rect')
            .data(d => d.map(v => ({ ...v, key: d.key, endpoint: v.data.name })))
            .enter().append('rect')
            .attr('x', d => x(d.endpoint))
            .attr('y', d => y(d[1]))
            .attr('height', d => y(d[0]) - y(d[1]))
            .attr('width', x.bandwidth())
            .on('mouseover', (event, d) => this._showTooltip(event, {
                key: d.key,
                value: d[1] - d[0],
                endpoint: d.endpoint
            }))
            .on('mouseout', () => this._hideTooltip());
        
        this._applyDarkModeStyles(g);
    }
    
    _renderHeatmap(data) {
        const container = this.container.node();
        const containerWidth = this.options.width || container.clientWidth;
        const { margin, height } = this.options;
        const width = containerWidth - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;
        
        // Clear and create SVG
        this.container.selectAll('*').remove();
        this.svg = this.container.append('svg')
            .attr('width', containerWidth)
            .attr('height', height);
        
        const g = this.svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
        
        const visibleUserTypes = this.userTypes.filter(ut => !this.hiddenUserTypes.has(ut));
        
        // Scales
        const x = d3.scaleBand()
            .domain(visibleUserTypes)
            .range([0, width])
            .padding(0.05);
        
        const y = d3.scaleBand()
            .domain(data.map(d => d.name))
            .range([0, innerHeight])
            .padding(0.05);
        
        // Color scale
        const maxValue = d3.max(data, d => d3.max(visibleUserTypes, ut => d[ut] || 0));
        const colorScale = d3.scaleSequential(d3.interpolateBlues)
            .domain([0, maxValue]);
        
        // Cells
        data.forEach(endpoint => {
            visibleUserTypes.forEach(userType => {
                const value = endpoint[userType] || 0;
                g.append('rect')
                    .attr('x', x(userType))
                    .attr('y', y(endpoint.name))
                    .attr('width', x.bandwidth())
                    .attr('height', y.bandwidth())
                    .attr('fill', value > 0 ? colorScale(value) : '#f3f4f6')
                    .attr('stroke', '#e5e7eb')
                    .attr('stroke-width', 1)
                    .on('mouseover', (event) => this._showTooltip(event, {
                        key: userType,
                        value: value,
                        endpoint: endpoint.name
                    }))
                    .on('mouseout', () => this._hideTooltip());
                
                // Add text for values > 0
                if (value > 0) {
                    g.append('text')
                        .attr('x', x(userType) + x.bandwidth() / 2)
                        .attr('y', y(endpoint.name) + y.bandwidth() / 2)
                        .attr('dy', '0.35em')
                        .attr('text-anchor', 'middle')
                        .attr('fill', value > maxValue * 0.5 ? 'white' : 'black')
                        .style('font-size', '10px')
                        .style('pointer-events', 'none')
                        .text(value);
                }
            });
        });
        
        // Axes
        g.append('g')
            .attr('transform', `translate(0,${innerHeight})`)
            .call(d3.axisBottom(x).tickFormat(ut => this.userTypeLabels[ut]))
            .selectAll('text')
            .style('text-anchor', 'middle');
        
        g.append('g')
            .call(d3.axisLeft(y))
            .selectAll('text')
            .style('font-size', '10px');
        
        this._applyDarkModeStyles(g);
    }
    
    _renderLegend() {
        const legendContainer = d3.select(`#${this.containerId}-legend`);
        if (legendContainer.empty()) {
            console.warn('Legend container not found');
            return;
        }
        
        legendContainer.selectAll('*').remove();
        
        const legend = legendContainer
            .append('div')
            .attr('class', 'flex flex-wrap gap-4 justify-center');
        
        this.userTypes.forEach(userType => {
            const item = legend.append('div')
                .attr('class', 'flex items-center gap-2 cursor-pointer')
                .style('opacity', this.hiddenUserTypes.has(userType) ? 0.4 : 1)
                .on('click', () => this._toggleUserType(userType));
            
            item.append('div')
                .style('width', '16px')
                .style('height', '16px')
                .style('background-color', this.colors[userType])
                .style('border-radius', '2px');
            
            item.append('span')
                .attr('class', 'text-sm text-gray-700 dark:text-gray-300')
                .text(this.userTypeLabels[userType]);
        });
    }
    
    _renderEmptyState() {
        this.container.html(`
            <div class="flex items-center justify-center h-full">
                <div class="text-center">
                    <p class="text-gray-500 dark:text-gray-400">No endpoint usage data available yet</p>
                    <p class="text-sm text-gray-400 dark:text-gray-500 mt-2">Statistics will appear as API endpoints are called</p>
                </div>
            </div>
        `);
    }
    
    _showTooltip(event, d) {
        const percentage = this.data.summary ? 
            ((d.value / this.data.summary.total_requests) * 100).toFixed(1) : 0;
        
        this.tooltip
            .style('visibility', 'visible')
            .html(`
                <div>
                    <div style="font-weight: 600; margin-bottom: 4px;">${d.endpoint}</div>
                    <div style="color: ${this.colors[d.key]};">${this.userTypeLabels[d.key]}: ${d.value} requests</div>
                    ${percentage > 0 ? `<div style="font-size: 11px; opacity: 0.8;">${percentage}% of total</div>` : ''}
                </div>
            `)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
    }
    
    _hideTooltip() {
        this.tooltip.style('visibility', 'hidden');
    }
    
    _toggleUserType(userType) {
        if (this.hiddenUserTypes.has(userType)) {
            this.hiddenUserTypes.delete(userType);
        } else {
            this.hiddenUserTypes.add(userType);
        }
        this.render();
    }
    
    _onBarClick(d) {
        console.log('Bar clicked:', d);
        // Emit custom event for external handling
        const event = new CustomEvent('endpoint-click', { 
            detail: { endpoint: d.endpoint, userType: d.key, value: d.value }
        });
        document.dispatchEvent(event);
    }
    
    _applyDarkModeStyles(g) {
        // Apply dark mode styles if body has dark class
        const isDark = document.body.classList.contains('dark') || 
                      document.documentElement.classList.contains('dark');
        
        if (isDark) {
            g.selectAll('.x-axis text, .y-axis text')
                .style('fill', '#d1d5db');
            g.selectAll('.x-axis path, .x-axis line, .y-axis path, .y-axis line')
                .style('stroke', '#4b5563');
        }
    }
    
    switchView(viewType) {
        this.options.view = viewType;
        this.render();
    }
    
    sortBy(criteria) {
        this.options.sortBy = criteria;
        this.render();
    }
    
    setTopN(n) {
        this.options.topN = n;
        this.render();
    }
    
    destroy() {
        if (this.tooltip) {
            this.tooltip.remove();
        }
        if (this.container) {
            this.container.selectAll('*').remove();
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EndpointStatsGraph;
}
