from rest_framework.routers import DefaultRouter

from apps.board.views import ColumnViewSet, ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("columns", ColumnViewSet, basename="column")
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
