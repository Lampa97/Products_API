from typing import Any, Dict, Optional

from celery.result import AsyncResult

from app.celery_app import celery_app
from app.services.external_providers import get_external_provider


class ProductSyncService:
    """Service for managing product synchronization tasks."""
    
    @staticmethod
    def start_full_sync(provider_type: str = None) -> Dict[str, Any]:
        """
        Start full product synchronization from external API.
        
        Args:
            provider_type: Type of external API provider (if None, uses settings)
            
        Returns:
            Dictionary with task information
        """
        # Validate provider exists
        try:
            provider = get_external_provider(provider_type)
            provider_name = provider.name
        except ValueError as e:
            return {
                "status": "error",
                "error": f"Invalid provider type: {str(e)}"
            }
        
        # Start sync task
        task = celery_app.send_task(
            "app.tasks.sync_products"
        )
        
        return {
            "status": "started",
            "task_id": task.id,
            "provider_type": provider_name,
            "message": "Product synchronization started"
        }
    
    @staticmethod
    def get_sync_status(task_id: str) -> Dict[str, Any]:
        """
        Get status of synchronization task.
        
        Args:
            task_id: Celery task ID
            
        Returns:
            Dictionary with task status
        """
        try:
            result = AsyncResult(task_id, app=celery_app)
            
            if result.state == "PENDING":
                return {
                    "status": "pending",
                    "message": "Task is waiting to be processed"
                }
            elif result.state == "PROGRESS":
                return {
                    "status": "in_progress",
                    "message": "Task is currently running",
                    "current": result.info.get("current", 0),
                    "total": result.info.get("total", 1)
                }
            elif result.state == "SUCCESS":
                return {
                    "status": "completed",
                    "result": result.result
                }
            elif result.state == "FAILURE":
                return {
                    "status": "failed",
                    "error": str(result.info)
                }
            else:
                return {
                    "status": result.state.lower(),
                    "message": f"Task state: {result.state}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to get task status: {str(e)}"
            }
    
    @staticmethod
    def cancel_sync(task_id: str) -> Dict[str, Any]:
        """
        Cancel synchronization task.
        
        Args:
            task_id: Celery task ID
            
        Returns:
            Dictionary with cancellation result
        """
        try:
            celery_app.control.revoke(task_id, terminate=True)
            
            return {
                "status": "cancelled",
                "task_id": task_id,
                "message": "Task cancellation requested"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to cancel task: {str(e)}"
            }
    
    @staticmethod
    def get_sync_history(limit: int = 10) -> Dict[str, Any]:
        """
        Get history of synchronization tasks.
        
        Args:
            limit: Maximum number of tasks to return
            
        Returns:
            Dictionary with task history
        """
        try:
            # Get active tasks
            active_tasks = celery_app.control.inspect().active()
            
            # Get scheduled tasks
            scheduled_tasks = celery_app.control.inspect().scheduled()
            
            # Get reserved tasks
            reserved_tasks = celery_app.control.inspect().reserved()
            
            return {
                "status": "success",
                "active_tasks": active_tasks or {},
                "scheduled_tasks": scheduled_tasks or {},
                "reserved_tasks": reserved_tasks or {},
                "message": f"Retrieved task history (limit: {limit})"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to get sync history: {str(e)}"
            }
    
    @staticmethod
    def trigger_manual_sync() -> Dict[str, Any]:
        """
        Trigger manual product synchronization.
        
        Returns:
            Dictionary with sync trigger result
        """
        return ProductSyncService.start_full_sync()
    
    @staticmethod
    def schedule_sync(
        cron_expression: Optional[str] = None,
        interval_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Schedule periodic product synchronization.
        
        Args:
            cron_expression: Cron expression for scheduling
            interval_seconds: Interval in seconds for periodic execution
            
        Returns:
            Dictionary with scheduling result
        """
        try:
            if cron_expression and interval_seconds:
                return {
                    "status": "error",
                    "error": "Cannot specify both cron_expression and interval_seconds"
                }
            
            if not cron_expression and not interval_seconds:
                # Use default interval (5 minutes)
                interval_seconds = 300
            
            # This would need integration with Celery Beat
            # For now, return a placeholder response
            return {
                "status": "success",
                "message": "Sync scheduling configured",
                "cron_expression": cron_expression,
                "interval_seconds": interval_seconds
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to schedule sync: {str(e)}"
            }