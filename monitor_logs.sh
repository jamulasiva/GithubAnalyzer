#!/bin/bash
# GitHub Audit Platform - Real-time Log Monitor
# Monitor all log files in real-time with colored output

LOGS_DIR="/home/sivaj/projects/AI-ML/AmzurGitHubAnalyzer/AmzurGitHubAnalyzer-WebHook/AmzurGitHubAnalyzer/logs"

echo "🚀 GitHub Audit Platform - Real-time Log Monitor"
echo "📂 Log directory: $LOGS_DIR"
echo "🔧 Available commands:"
echo "  ./monitor_logs.sh app     - Monitor application.log"
echo "  ./monitor_logs.sh db      - Monitor database.log" 
echo "  ./monitor_logs.sh webhook - Monitor webhook_events.log"
echo "  ./monitor_logs.sh error   - Monitor errors.log"
echo "  ./monitor_logs.sh all     - Monitor all logs (multitail)"
echo ""

# Function to check if log file exists
check_log_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "❌ Log file not found: $file"
        echo "💡 Start the backend server to generate log files"
        exit 1
    fi
}

case "${1:-all}" in
    "app"|"application")
        LOG_FILE="$LOGS_DIR/application.log"
        check_log_file "$LOG_FILE"
        echo "📋 Monitoring application.log (Ctrl+C to stop)"
        tail -f "$LOG_FILE"
        ;;
    "db"|"database")
        LOG_FILE="$LOGS_DIR/database.log"
        check_log_file "$LOG_FILE"
        echo "🗄️  Monitoring database.log (Ctrl+C to stop)"
        tail -f "$LOG_FILE"
        ;;
    "webhook"|"webhooks")
        LOG_FILE="$LOGS_DIR/webhook_events.log"
        check_log_file "$LOG_FILE"
        echo "🔗 Monitoring webhook_events.log (Ctrl+C to stop)"
        tail -f "$LOG_FILE"
        ;;
    "error"|"errors")
        LOG_FILE="$LOGS_DIR/errors.log"
        check_log_file "$LOG_FILE"
        echo "❌ Monitoring errors.log (Ctrl+C to stop)"
        tail -f "$LOG_FILE"
        ;;
    "all")
        echo "🔄 Monitoring all log files simultaneously..."
        
        # Check if multitail is available
        if command -v multitail >/dev/null 2>&1; then
            multitail \
                -t "🚀 APPLICATION" "$LOGS_DIR/application.log" \
                -t "🗄️  DATABASE" "$LOGS_DIR/database.log" \
                -t "🔗 WEBHOOKS" "$LOGS_DIR/webhook_events.log" \
                -t "❌ ERRORS" "$LOGS_DIR/errors.log"
        else
            echo "⚠️  multitail not available, using tail for application.log"
            echo "💡 Install multitail for better multi-log monitoring: sudo apt install multitail"
            echo ""
            tail -f "$LOGS_DIR/application.log"
        fi
        ;;
    *)
        echo "❌ Invalid option: $1"
        echo "💡 Use: app, db, webhook, error, or all"
        exit 1
        ;;
esac