-- Performance Metrics Table
-- Frontend performance metrics (Core Web Vitals, custom metrics)

CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value REAL NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    metric_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_performance_metrics_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS ix_performance_metrics_user_name ON performance_metrics (user_id, metric_name);
CREATE INDEX IF NOT EXISTS ix_performance_metrics_timestamp ON performance_metrics (timestamp);
CREATE INDEX IF NOT EXISTS ix_performance_metrics_created_at ON performance_metrics (created_at);
CREATE INDEX IF NOT EXISTS ix_performance_metrics_id ON performance_metrics (id);
CREATE INDEX IF NOT EXISTS ix_performance_metrics_user_id ON performance_metrics (user_id);
CREATE INDEX IF NOT EXISTS ix_performance_metrics_metric_name ON performance_metrics (metric_name);
