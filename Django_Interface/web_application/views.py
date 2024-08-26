from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from .MongoListInterface import MongoListInterface
from .MongoSearchInterface import MongoSearchInterface
from .MongoStatsInterface import MongoStatsInterface
from pathlib import Path

def logger(current_time:str, start_date:str, end_date:str, telegram_channels:list, factual:bool, response_size:int):
    def make_path(extension: str) -> str:
        project_path = Path(Path(__file__).resolve().parent)
        return str(project_path / extension)
    s = "\n----------------------------\n"
    s+= f"Time of request: {current_time}.\n"
    s+= f"Requested start date: {start_date}.\n"
    s+= f"Requested end date: {end_date}.\n"
    if factual:
        s+= f"Only factual posts requested.\n"
    if len(telegram_channels) == 0:
        s+= f"All Telegram channels requested.\n"
    else:
        s+= f"Requested Telegram channels:\n"
        for channel in telegram_channels:
            s+= f"{channel}\n"
    s += f"Number of posts returned: {response_size}.\n"
    s += "----------------------------\n"
    with open(make_path("custom_log.txt"), 'a') as file:
        file.write(s)

class CustomPagination(PageNumberPagination):
    page_size = 3000  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 30000  # Maximum number of items per page

class ListDataView(APIView):
    """
    API view to handle requests with start_date, end_date, and optional telegram_channels.
    Returns either a paginated list or the entire list of dictionaries based on the pagination argument.
    """

    def get(self, request):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        telegram_channels = request.query_params.getlist('telegram_channels', [])
        factual = request.query_params.get('factual', 'false').lower() == 'true'
        pagination = request.query_params.get('pagination', 'false').lower() == 'true'
        remove_russian = request.query_params.get('remove_russian', 'true').lower() == 'true'

        data = MongoListInterface().get_daterange_docs(start_date=start_date, end_date=end_date, collection_names=telegram_channels, factual=factual, remove_russian=remove_russian)
        
        #response_size = len(data)
        #logger(current_time=current_time, start_date=start_date, end_date=end_date, telegram_channels=telegram_channels, factual=factual, response_size=response_size)

        if pagination:
            # Apply pagination if the pagination flag is True
            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(data, request)
            return paginator.get_paginated_response(paginated_data)
        else:
            # Return the entire data if pagination is False
            return Response(data, status=status.HTTP_200_OK)

class SearchDataView(APIView):
    """
    API view to handle requests with query text for the search function.
    Returns a list of dictionaries.
    """
    def get(self, request):
        query_text = request.query_params.get('query_text')
        data = MongoSearchInterface().search(query_text=query_text)
        return Response(data, status=status.HTTP_200_OK)
    
class GetStatsView(APIView):
    """
    API view to handle requests with query text for the trend function.
    Returns a list of dictionaries.
    """
    def get(self, request):
        start_day = request.query_params.get('start_day')
        end_day = request.query_params.get('end_day')
        channel_names = request.query_params.get('channel_names')
        data = MongoStatsInterface().fetch_documents_by_date_range(start_day=start_day, end_day=end_day, channel_names=channel_names)
        print(data)
        return Response(data, status=status.HTTP_200_OK) 