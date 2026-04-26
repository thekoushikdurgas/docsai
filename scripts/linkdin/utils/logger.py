"""
Logging Utilities Module
Provides comprehensive logging setup and management for the application.
Enhanced with file rotation, multiple handlers, and structured logging.
"""

import logging
import logging.handlers
import os
import sys
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import json
from dataclasses import dataclass
from enum import Enum

class LogLevel(Enum):
    """Enum for log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class LoggingConfig:
    """Configuration for logging setup"""
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "./logs/app.log"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5
    enable_console: bool = True
    enable_file: bool = True
    enable_json: bool = False
    enable_structured: bool = False

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        if hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                          'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process', 'getMessage']:
                log_entry[key] = value
        
        return json.dumps(log_entry)

class StructuredFormatter(logging.Formatter):
    """Structured formatter for better log parsing"""
    
    def format(self, record):
        # Create structured log entry
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage()
        }
        
        # Add context information
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Format as key=value pairs
        formatted_parts = []
        for key, value in log_entry.items():
            if isinstance(value, str) and ' ' in value:
                formatted_parts.append(f"{key}='{value}'")
            else:
                formatted_parts.append(f"{key}={value}")
        
        return ' '.join(formatted_parts)

class LoggerManager:
    """
    Logger manager for setting up and managing application logging.
    """
    
    def __init__(self, config: Optional[LoggingConfig] = None):
        """
        Initialize logger manager.
        
        Args:
            config: Logging configuration
        """
        self.config = config or LoggingConfig()
        self.loggers: Dict[str, logging.Logger] = {}
        self.handlers: List[logging.Handler] = []
        
        # Create logs directory
        self._create_logs_directory()
        
        # Setup root logger
        self._setup_root_logger()
    
    def _create_logs_directory(self):
        """Create logs directory if it doesn't exist."""
        try:
            log_dir = Path(self.config.file_path).parent
            log_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error creating logs directory: {e}")
    
    def _setup_root_logger(self):
        """Setup root logger with handlers."""
        try:
            # Get root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(getattr(logging, self.config.level.value))
            
            # Clear existing handlers
            root_logger.handlers.clear()
            
            # Setup console handler
            if self.config.enable_console:
                console_handler = self._create_console_handler()
                root_logger.addHandler(console_handler)
                self.handlers.append(console_handler)
            
            # Setup file handler
            if self.config.enable_file:
                file_handler = self._create_file_handler()
                root_logger.addHandler(file_handler)
                self.handlers.append(file_handler)
            
            # Setup error file handler
            error_handler = self._create_error_handler()
            root_logger.addHandler(error_handler)
            self.handlers.append(error_handler)
            
        except Exception as e:
            print(f"Error setting up root logger: {e}")
    
    def _create_console_handler(self) -> logging.StreamHandler:
        """Create console handler with colored output."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, self.config.level.value))
        
        if self.config.enable_json:
            formatter = JSONFormatter()
        elif self.config.enable_structured:
            formatter = StructuredFormatter()
        else:
            formatter = ColoredFormatter(self.config.format)
        
        console_handler.setFormatter(formatter)
        return console_handler
    
    def _create_file_handler(self) -> logging.handlers.RotatingFileHandler:
        """Create rotating file handler."""
        file_handler = logging.handlers.RotatingFileHandler(
            self.config.file_path,
            maxBytes=self.config.max_file_size,
            backupCount=self.config.backup_count
        )
        file_handler.setLevel(getattr(logging, self.config.level.value))
        
        if self.config.enable_json:
            formatter = JSONFormatter()
        elif self.config.enable_structured:
            formatter = StructuredFormatter()
        else:
            formatter = logging.Formatter(self.config.format)
        
        file_handler.setFormatter(formatter)
        return file_handler
    
    def _create_error_handler(self) -> logging.handlers.RotatingFileHandler:
        """Create error file handler for ERROR and CRITICAL messages."""
        error_file = str(Path(self.config.file_path).parent / "error.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=self.config.max_file_size,
            backupCount=self.config.backup_count
        )
        error_handler.setLevel(logging.ERROR)
        
        if self.config.enable_json:
            formatter = JSONFormatter()
        elif self.config.enable_structured:
            formatter = StructuredFormatter()
        else:
            formatter = logging.Formatter(self.config.format)
        
        error_handler.setFormatter(formatter)
        return error_handler
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get or create a logger with the specified name.
        
        Args:
            name: Logger name
            
        Returns:
            Logger instance
        """
        if name not in self.loggers:
            logger = logging.getLogger(name)
            self.loggers[name] = logger
        
        return self.loggers[name]
    
    def setup_module_logger(self, module_name: str, level: Optional[LogLevel] = None) -> logging.Logger:
        """
        Setup logger for a specific module.
        
        Args:
            module_name: Name of the module
            level: Log level for the module
            
        Returns:
            Logger instance
        """
        logger = self.get_logger(module_name)
        
        if level:
            logger.setLevel(getattr(logging, level.value))
        
        return logger
    
    def add_context(self, logger: logging.Logger, **context):
        """
        Add context information to logger.
        
        Args:
            logger: Logger instance
            **context: Context information to add
        """
        for key, value in context.items():
            setattr(logger, key, value)
    
    def log_function_call(self, logger: logging.Logger, func_name: str, 
                         args: tuple = (), kwargs: dict = None, level: LogLevel = LogLevel.DEBUG):
        """
        Log function call with arguments.
        
        Args:
            logger: Logger instance
            func_name: Name of the function
            args: Function arguments
            kwargs: Function keyword arguments
            level: Log level
        """
        if kwargs is None:
            kwargs = {}
        
        args_str = ', '.join([str(arg) for arg in args])
        kwargs_str = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
        
        params = []
        if args_str:
            params.append(args_str)
        if kwargs_str:
            params.append(kwargs_str)
        
        params_str = ', '.join(params)
        message = f"Calling {func_name}({params_str})"
        
        logger.log(getattr(logging, level.value), message)
    
    def log_performance(self, logger: logging.Logger, operation: str, 
                       duration: float, level: LogLevel = LogLevel.INFO):
        """
        Log performance metrics.
        
        Args:
            logger: Logger instance
            operation: Name of the operation
            duration: Duration in seconds
            level: Log level
        """
        message = f"Performance: {operation} took {duration:.4f} seconds"
        logger.log(getattr(logging, level.value), message)
    
    def log_error_with_context(self, logger: logging.Logger, error: Exception, 
                              context: Dict[str, Any] = None, level: LogLevel = LogLevel.ERROR):
        """
        Log error with additional context.
        
        Args:
            logger: Logger instance
            error: Exception to log
            context: Additional context information
            level: Log level
        """
        message = f"Error: {str(error)}"
        
        if context:
            context_str = ', '.join([f"{k}={v}" for k, v in context.items()])
            message += f" | Context: {context_str}"
        
        logger.log(getattr(logging, level.value), message, exc_info=True)
    
    def get_log_stats(self) -> Dict[str, Any]:
        """
        Get logging statistics.
        
        Returns:
            Dictionary with logging statistics
        """
        stats = {
            'total_loggers': len(self.loggers),
            'total_handlers': len(self.handlers),
            'config': {
                'level': self.config.level.value,
                'file_path': self.config.file_path,
                'max_file_size': self.config.max_file_size,
                'backup_count': self.config.backup_count,
                'enable_console': self.config.enable_console,
                'enable_file': self.config.enable_file,
                'enable_json': self.config.enable_json,
                'enable_structured': self.config.enable_structured
            }
        }
        
        return stats
    
    def update_config(self, new_config: LoggingConfig):
        """
        Update logging configuration.
        
        Args:
            new_config: New logging configuration
        """
        self.config = new_config
        self._setup_root_logger()
    
    def close_handlers(self):
        """Close all logging handlers."""
        for handler in self.handlers:
            handler.close()

# Global logger manager instance
logger_manager = LoggerManager()

def setup_logger(name: str, level: Optional[LogLevel] = None) -> logging.Logger:
    """
    Setup logger for a module.
    
    Args:
        name: Logger name
        level: Log level
        
    Returns:
        Logger instance
    """
    return logger_manager.setup_module_logger(name, level)

def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logger_manager.get_logger(name)

def log_function_call(logger: logging.Logger, func_name: str, 
                     args: tuple = (), kwargs: dict = None, level: LogLevel = LogLevel.DEBUG):
    """Log function call with arguments."""
    logger_manager.log_function_call(logger, func_name, args, kwargs, level)

def log_performance(logger: logging.Logger, operation: str, 
                   duration: float, level: LogLevel = LogLevel.INFO):
    """Log performance metrics."""
    logger_manager.log_performance(logger, operation, duration, level)

def log_error_with_context(logger: logging.Logger, error: Exception, 
                          context: Dict[str, Any] = None, level: LogLevel = LogLevel.ERROR):
    """Log error with additional context."""
    logger_manager.log_error_with_context(logger, error, context, level)

# Decorator for automatic function logging
def log_function_calls(level: LogLevel = LogLevel.DEBUG):
    """
    Decorator to automatically log function calls.
    
    Args:
        level: Log level for function calls
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            log_function_call(logger, func.__name__, args, kwargs, level)
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Function {func.__name__} completed successfully")
                return result
            except Exception as e:
                log_error_with_context(logger, e, {
                    'function': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                })
                raise
        
        return wrapper
    return decorator

# Decorator for performance logging
def log_performance_metrics(operation_name: Optional[str] = None):
    """
    Decorator to automatically log performance metrics.
    
    Args:
        operation_name: Name of the operation (defaults to function name)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            op_name = operation_name or func.__name__
            
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                log_performance(logger, op_name, duration)
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                log_performance(logger, f"{op_name} (failed)", duration, LogLevel.ERROR)
                raise
        
        return wrapper
    return decorator

# Usage example
if __name__ == "__main__":
    # Example usage
    config = LoggingConfig(
        level=LogLevel.DEBUG,
        enable_console=True,
        enable_file=True,
        enable_structured=True
    )
    
    manager = LoggerManager(config)
    
    # Get logger
    logger = manager.get_logger("test_module")
    
    # Test logging
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test function call logging
    @log_function_calls(LogLevel.DEBUG)
    def test_function(x, y, z=None):
        return x + y
    
    result = test_function(1, 2, z=3)
    print(f"Result: {result}")
    
    # Test performance logging
    @log_performance_metrics("test_operation")
    def slow_function():
        import time
        time.sleep(0.1)
        return "done"
    
    result = slow_function()
    print(f"Slow function result: {result}")
    
    # Get stats
    stats = manager.get_log_stats()
    print(f"Logger stats: {stats}")
