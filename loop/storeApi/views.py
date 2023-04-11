from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StoreStatus, Timing, Timezone, Report
from datetime import datetime, timedelta
from collections import defaultdict
from .serializers import ReportSerializer
import pytz
import random
import string

reportId ={}
# Create your views here.
class TriggerReport(APIView):

    def get(self, request):

        # variables to store the total uptime and downtime for each time period
        uptime_last_hour= 0
        downtime_last_hour= 0
        uptime_last_day= 0
        downtime_last_day= 0
        uptime_last_week= 0
        downtime_last_week= 0

        # current time in UTC
        now= datetime.now(pytz.timezone('UTC'))

        #for last hour

        #calculating timestamps
        hour_ago= now - timedelta(hours=1)
        # calculating the uptime and downtime 
        hour_data= calc(hour_ago.timestamp(), now.timestamp())
        # storing the uptime and downtime in variables
        uptime_last_hour= hour_data['uptime']
        downtime_last_hour= hour_data['downtime']

        #for last day

        #calculating timestamps
        day_starting = (now - timedelta(days=1))
        day_starting = datetime(day_starting.year, day_starting.month, day_starting.day)
        day_starting= pytz.timezone('UTC').localize(day_starting)
        day_ending= day_starting + timedelta(days=1, microseconds=-1)

        # print(day_starting, day_ending, 'day_starting, day_ending')
        # calculating the uptime and downtime
        day_data = calc(day_starting.timestamp(), day_ending.timestamp())
        # storing the uptime and downtime in variables
        uptime_last_day= day_data['uptime']
        downtime_last_day= day_data['downtime']
        

        #for last week
        #calculating timestamps
        week_starting = now - timedelta(days=now.weekday() + 7)
        week_starting = datetime(week_starting.year, week_starting.month, week_starting.day)
        week_starting = pytz.timezone('UTC').localize(week_starting)
        week_ending= week_starting + timedelta(days=7, microseconds=-1)
        # print(week_starting, week_ending, 'week_starting, week_ending')
        # calculating the uptime and downtime
        week_data = calc(week_starting.timestamp(), week_ending.timestamp())
        # storing the uptime and downtime in variables
        uptime_last_week= week_data['uptime']
        downtime_last_week= week_data['downtime']

       
        # Generate a random string of specified length
        random_string = ''.join(random.choice(string.ascii_letters) for _ in range(10))    
        # Create a new Report object and save it to the database        
        report=  Report.objects.create(
            report_string= random_string,
            uptime_last_hour= uptime_last_hour,
            downtime_last_hour= downtime_last_hour,
            uptime_last_day= uptime_last_day,
            downtime_last_day= downtime_last_day,
            uptime_last_week= uptime_last_week,
            downtime_last_week= downtime_last_week
        )
        report.save()
        
        # Return the random string
        return Response(f'Report id: {random_string}')

class GetReport(APIView):
    def post(self, request):
        #get the report id from the request
        data=request.data['reportId']
        #fetch the report from the database and serialize it
        serializer = ReportSerializer(Report.objects.get(report_string=data))
        #return the serialized report
        return Response(serializer.data)
    

# Function to calculate the uptime and downtime for a given time period
def calc(given_start_timestamp, given_end_timestamp):
    uptime= 0
    downtime= 0
    # Retrieve all StoreStatus objects between the given timestamps
    #print(given_start_timestamp, given_end_timestamp, 'given_start_timestamp, given_end_timestamp')
    store_statuses = StoreStatus.objects.filter(
        timestamp_utc__range=(
        pytz.timezone('UTC').localize(datetime.utcfromtimestamp(given_start_timestamp)), 
        pytz.timezone('UTC').localize(datetime.utcfromtimestamp(given_end_timestamp)))).order_by('timestamp_utc')

    # Create a defaultdict to group StoreStatus objects by store_id
    store_status_groups = defaultdict(list)

    # Iterate through all StoreStatus objects and group them by store_id
    for store_status in store_statuses:
        store_status_groups[store_status.store_id].append(store_status)


    # Iterate through the grouped store_status_groups dictionary
    for store_id, store_status_group in store_status_groups.items():
        print(store_id, store_status_group, 'store_status_group')

        # Get the timezone string for the current store 
        try:
            timezone_str = Timezone.objects.get(store_id=store_id).timezone_str
        except Timezone.DoesNotExist:
            timezone_str = 'America/Chicago'

        # Iterate through the days of the week
        for day in range(7):
            # Get the start and end times for the current store and day
            try:
                start_time_local = Timing.objects.get(store_id=store_id, day=day).start_time_local
            except:
                start_time_local = datetime.strptime('00:00:00', '%H:%M:%S').time()
            
            try:
                end_time_local = Timing.objects.get(store_id=store_id, day=day).end_time_local
            except:
                end_time_local = datetime.strptime('23:59:59', '%H:%M:%S').time()

            # Get the timestamps to start the search from
            start_timestamp= get_initial_timestamp_day(start_time_local, timezone_str, day)
            end_timestamp= get_initial_timestamp_day(end_time_local, timezone_str, day)
            print(f'start_timestamp: {start_timestamp}, end_timestamp: {end_timestamp}')

            # Iterate through the business hours and find overlap with given timestamps
            while(start_timestamp<given_end_timestamp):
                if end_timestamp>given_start_timestamp:

                    # Calculate the uptime and downtime for this overlap
                    temp = calculate_uptime_downtime(store_id, max(start_timestamp, given_start_timestamp), min(end_timestamp, given_end_timestamp), store_status_group)

                    # Add the uptime and downtime to the total uptime and downtime
                    uptime += temp['uptime']
                    downtime += temp['downtime']
                
                # Increment the timestamps by 7 days
                start_timestamp += 7*24*60*60
                end_timestamp += 7*24*60*60
                print(f'start_timestamp: {start_timestamp}, end_timestamp: {end_timestamp}')
        # break
    # Return the uptime and downtime
    return {'uptime': uptime, 'downtime': downtime}

# Function to get the timestamp to start the search from
def get_initial_timestamp_day(time_str, timezone_str, day):
    # print(datetime.now(pytz.timezone('UTC')))
    # Get current day and time in given timezone
    current_timestamp = datetime.now(pytz.timezone(timezone_str))

    # Get the timestamp for the start 
    days_to_substract = (current_timestamp.weekday() - day +7)%7 + 14
    timestamp_start_day = current_timestamp - timedelta(days=days_to_substract)
    start_timestamp_day = timestamp_start_day.replace(hour=time_str.hour, minute=time_str.minute, second=time_str.second, microsecond=0)
    # print(start_timestamp_day.timestamp(), 'start_timestamp_day')
    return start_timestamp_day.timestamp()

# Function to calculate the uptime and downtime for a given time period
def calculate_uptime_downtime(store_id, start_timestamp, end_timestamp, this_store_query_set):
    print(f'1st: {start_timestamp}, 2nd: {end_timestamp}')
    last = start_timestamp
    uptime= 0
    downtime= 0
    # utc_start_date = pytz.timezone('UTC').localize(datetime.utcfromtimestamp(start_timestamp))
    # utc_end_date = pytz.timezone('UTC').localize(datetime.utcfromtimestamp(end_timestamp))
    # ent = this_store_query_set.filter(timestamp_utc__range=(utc_start_date, utc_end_date) , store_id=store_id).order_by('timestamp_utc') 
    # print(ent)
    for i in this_store_query_set:
        if(i.timestamp_utc.timestamp() > end_timestamp or i.timestamp_utc.timestamp() < start_timestamp):
            continue
        if i.status=='active':
            # print(uptime)
            # print(i.timestamp_utc.timestamp(), last, i.timestamp_utc.timestamp() - last)
            uptime += i.timestamp_utc.timestamp() - last
        else:
            # print(downtime)
            # print(i.timestamp_utc.timestamp(), last, i.timestamp_utc.timestamp() - last)
            downtime += i.timestamp_utc.timestamp() - last
        last = i.timestamp_utc.timestamp()
        
    if(len(this_store_query_set) > 0):
        ent = this_store_query_set[len(this_store_query_set)-1]
        if(ent.timestamp_utc.timestamp() <= end_timestamp and ent.timestamp_utc.timestamp() >=start_timestamp):
            if(ent.status == 'active'):
                uptime += end_timestamp - last
            else:
                downtime += end_timestamp - last

    print(uptime, 'uptime')
    print(downtime, 'downtime')
    return {'uptime': uptime, 'downtime': downtime}



















    # Alternate
    # get all the stores and their timezone informations
        # stores = {}
        # for store in Timezone.objects.all():
        #     timezone_str = store.timezone_str or 'America/Chicago'
        #     stores[store.store_id]= timezone_str

        # # loop through all stores
        # for store_id, timezone_str in stores.items():
        #     # get the business hours of the store
        #     business_week = Timing.objects.filter(store_id=store_id)
        #     this_store_query_set = StoreStatus.objects.filter(store_id=store_id)
        #     for business_day in business_week:
        #         print(business_day, 'business_day')
        #         start_time_local = business_day.start_time_local or datetime.strptime('00:00:00', '%H:%M:%S').time()
        #         end_time_local = business_day.end_time_local or datetime.strptime('23:59:59', '%H:%M:%S').time()

        #         start_timestamp= get_initial_timestamp_day(start_time_local, timezone_str, business_day.day)
        #         end_timestamp= get_initial_timestamp_day(end_time_local, timezone_str, business_day.day)
        #         print(f'start_timestamp: {start_timestamp}, end_timestamp: {end_timestamp}')

        #         while(start_timestamp<previous_day_ending_timestamp):
        #             if end_timestamp>previous_day_starting_timestamp:
        #                 temp = calculate_uptime_downtime(store_id, max(start_timestamp, previous_day_starting_timestamp), min(end_timestamp, previous_day_ending_timestamp), this_store_query_set)
        #                 total_uptime_last_day += temp['uptime']
        #                 total_downtime_last_day += temp['downtime']
        #             start_timestamp += 7*24*60*60
        #             end_timestamp += 7*24*60*60
        #             print(f'start_timestamp: {start_timestamp}, end_timestamp: {end_timestamp}')