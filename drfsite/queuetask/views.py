from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .scheduler import scheduler
import csv
import os
from datetime import datetime
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (
    HumanSerializer,
    QueueEntrySerializer,
    IDSerializer,
    OperationSerializer,
)
from .application_service import (
    create_queue,
    add_user_to_queue,
    get_queue_entries,
    notify_user,
    serve_user,
    queues,
)
from .operation_service import (
    create_operation,
    finish_operation,
    get_operation,
)

@extend_schema_view(
    get_queue=extend_schema(
        summary="Get a list of queue entries",
        responses={
            200: HumanSerializer(many=True),
            404: None,
        }
    ),
    create=extend_schema(
        summary="Create a new queue",
        request=IDSerializer,
        responses={
            201: QueueEntrySerializer,
        }
    ),
    add_user_to_queue=extend_schema(
        summary="Add a user to an existing queue",
        responses={
            201: QueueEntrySerializer,
        }
    ),
    notify=extend_schema(
        summary="Notify a user about their queue entry",
        responses={
            200: HumanSerializer,
            404: None,
        }
    ),
    serve=extend_schema(
        summary="Serve a user from the queue",
        responses={
            200: HumanSerializer,
            404: None,
        }
    ),

)
class QueueEntryViewSet(ViewSet):
    def get_queue(self, _, queue_id):

        entries = get_queue_entries(queue_id)
        if entries is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = HumanSerializer(entries, many=True)
            return Response(serializer.data)



    def create(self, request):
        serializer = IDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tt = create_queue(queue_id=serializer.validated_data['id'])
        response_serializer = QueueEntrySerializer(tt)
        return Response(response_serializer.data,status=status.HTTP_201_CREATED)

    def add_user_to_queue(self, _, queue_id, user_id):
        tt=add_user_to_queue(queue_id, user_id)
        response_serializer = QueueEntrySerializer(tt)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def notify(self,_, queue_id, user_id):
        try:
            entry = notify_user(queue_id, user_id)
            serializer = HumanSerializer(entry)
            return Response(serializer.data)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def serve(self,_, queue_id, user_id):
        try:
            entry = serve_user(queue_id, user_id)
            serializer = HumanSerializer(entry)
            return Response(serializer.data)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get an operation by ID",
        responses={
            200: OperationSerializer,
            404: None,
        }
    ),
    export_data=extend_schema(
        summary="Export data for an operation",
        responses={
            202: None,
        }
    ),
)
class OperationsViewSet(ViewSet):

    def retrieve(self, request, operation_id):
        try:
            operation = get_operation(operation_id)
            serializer = OperationSerializer(operation)
            return Response(serializer.data)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def export_data(self, request):
        operation_id = create_operation()

        # Запланировать задачу выгрузки данных в фоновом режиме
        scheduler.add_job(
            self._export_data_task,
            args=[operation_id],
            id=str(operation_id),
            replace_existing=True,
        )

        return Response({'operation_id': str(operation_id)}, status=status.HTTP_202_ACCEPTED)

    def _export_data_task(self, operation_id):
        try:
            # Получить все записи во всех очередях
            all_queue_entries = []

            for queue_id, entries in queues.items():
                all_queue_entries.append(entries)

            # Создать имя файла с текущей датой и временем
            filename = f"queue_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            file_path = f"queuetask//reports//{filename}"

            # Выгрузить данные в CSV-файл
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['id', 'user_ids', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for entry in all_queue_entries:
                    writer.writerow({
                        'id': str(entry.id),
                        'user_ids': '| '.join(str(user_id.id) for user_id in entry.user_ids),
                        'created_at': entry.created_at.isoformat(),
                    })

            # Завершить операцию и сохранить результат
            finish_operation(operation_id, {'file': filename})
        except Exception as e:
            # В случае ошибки завершить операцию с ошибкой
            finish_operation(operation_id, {'error': str(e)})
