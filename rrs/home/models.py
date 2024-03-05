from django.db import models
from datetime import datetime,date

# Create your model

class user_master(models.Model):
    firstname=models.CharField("First Name",max_length=50)
    lastname=models.CharField("Last Name", max_length=50,blank=True)
    username = models.CharField("Username", max_length=50)
    password = models.CharField("Password",max_length=128)
    dob=models.DateField()
    email = models.EmailField()
    mobile=models.IntegerField()
    address=models.TextField()
    regis_date=models.DateField(default=date.today())
    
    def __str__(self):
        return self.username
    class Meta:
        db_table = "user_master"
        
class blogs(user_master):
    title = models.CharField('Blog Title',max_length=200)
    content = models.TextField('Content')
    pub_date = models.DateTimeField('Date Published',auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.title} by {self.username}'
class station_master(models.Model):
    station_id=models.AutoField(primary_key=True)
    station_name=models.CharField(max_length=30,null=False)
    station_code=models.CharField(unique=True,max_length=5, null=False)
    location = models.CharField(max_length=50,null=False)
    zone=models.CharField(max_length=30,null=False)
    state=models.CharField(max_length=20,null=False)

    def __str__(self) :
        return self.station_name
    class Meta:
        db_table= "station_master"  # specify the table name in database if not same as ClassName  
class train_schedule(models.Model):  # inherit the properties of the parent class
    train_no=models.ForeignKey(station_master,on_delete=models.CASCADE)
    depart_time=models.TimeField()
    arrival_time=models.TimeField()
    platform=models.CharField(max_length=10)
    status=models.BooleanField(default=False)   # True for running and False for stopped

    def get_train_platform(self):
        if self.status==True:
            return self.platform+" Platform"
        else:
            return "Platform is not assigned"

    def get_arrival_time(self):
        current_time=datetime.now().time()
        diff=current_time - self.start_time
        minutes=diff.seconds//60+diff.days*24*60
        hours,remaining_minutes=divmod(minutes,60)
        return f"Train will arrive in {hours} hour(s) and {remaining_minutes} minute(s)"

    class Meta:
        verbose_name="Train Schedule"
        verbose_name_plural="Trains Schedules"

# for feedback
class  user_feedback(models.Model):
    username=models.CharField(max_length=30)
    subject=models.CharField(max_length=100)
    message=models.TextField()

    def  __str__(self):
        return self.username + "-"+self.subject
    class Meta:
        db_table= 'user_feedback'

# for train_master model
class  train_master(models.Model):
    train_no  = models.IntegerField(primary_key=True)
    train_name = models.CharField(max_length=50, null = False)
    source_station=models.ForeignKey(station_master, related_name="source_station", on_delete=models.CASCADE, verbose_name="Source Station")
    dest_station = models.ForeignKey(station_master, on_delete=models.SET_NULL, related_name='dest_station', null=True, blank=True)
    depart_datetime = models.DateTimeField()
    arrival_datetime=models.DateTimeField()
    journey_duration=models.DurationField()
    available_seats=models.PositiveSmallIntegerField()
    total_seats = models.PositiveBigIntegerField()
    
    def  __str__(self):
        return  f'{self.train_name}-{self.depart_datetime}'
        
    class Meta:
        db_table =  'train_master'

    '''@staticmethod
    def create_new_trains(data):
        try:
            new_train = train_mastership(**data)
            new_train.save()
            return {"id":new_train.train_no,"message":"New Train Created Successfully!"},201
        except Exception as e:
            return{"error":"Error Creating New Train"},400

    @staticmethod
    def update_train_info(train_no, data):
        try:
            with transaction.atomic():
                queryset = train_mastership.objects.select_for_update().get(train_no=train_no)
                for key,value in data.items():
                    setattr(queryset,key,value)
                queryset.save()
                return {"message":"Train Information Updated Successfully!"},200
        except ObjectDoesNotExist:
            return{"error":"No such train exists."},404
        except Exception as e:
            return{"error":str(e)},500

    @staticmethod
    def get_all_trains():
        all_trains = [train_mastership_serialize(train).data for train in train_mastership.objects.all()]
        return {"count":len(all_trans),"results":all_trains}

    @staticmethod
    def delete_a_train(train_no):
        try:
            train = train_mastership.objects.get(train_no=train_no)
            train.delete()
            return {"message":"Train Deleted Successfully!"},200
        except ObjectDoesNotExist:
            return{"error":"The specified train does not exist."},404
        except Exception as e:
            return{"error":str(e)},500  '''

# passenger models
class passenger_master(models.Model):
    pass_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=6)
    class Meta:
        db_table = "passenger_master"
    
class class_master(models.Model):
    class_id = models.IntegerField(primary_key=True)
    class_name = models.CharField(max_length=10)
    class_name = models.CharField(max_length=20,null=False)
    description= models.TextField(max_length=100)
    features = models.TextField(max_length=100)
    capacity = models.IntegerField()
    price = models.FloatField()
    class Meta:
        db_table = "class_master"



class RouteMaster(models.Model):
    route_id = models.AutoField(primary_key=True)
    source_station = models.ForeignKey('station_master', on_delete=models.CASCADE, related_name='source_routes')
    destination_station = models.ForeignKey('station_master', on_delete=models.CASCADE, related_name='destination_routes')
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    route_name = models.CharField(max_length=255, blank=True, null=True)
    travel_time = models.DurationField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.source_station.station_name} to {self.destination_station.station_name}"
    class Meta:
        db_table = "route_master"

class routestation(models.Model):
    train_no = models.ForeignKey('train_master',on_delete=models.CASCADE)
    station_id = models.ForeignKey('station_Master', on_delete=models.PROTECT)
    sequence_no = models.PositiveSmallIntegerField() # Sequence number of the station in a train journey
                                                # 1 means it is the first station and so on.
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    class Meta:
        ordering = ['sequence_no']
        db_table="route_stations"


# A Train can have multiple schedules for different days
class ScheduleMaster(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    train_no = models.ForeignKey('train_master',on_delete=models.PROTECT)
    route_id = models.ForeignKey('RouteMaster',on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    # If this field is not provided then we assume that the train runs everyday from the start date till the end date.
    # If this field is not provided then we assume that it runs everyday from start date till end date.
    weekdays=[
        ("Monday", "Monday"),
        ("Tuesday","Tuesday"),
        ("Wednesday","Wednesday"),
        ("Thursday","Thursday"),
        ("Friday","Friday"),
        ("Saturday","Saturday"),
        ("Sunday","Sunday")
      ]
    week = models.CharField(max_length=9, choices=[item for item in weekdays])

    @property
    def get_weekday(self):
        if self.week == 'Monday':
            return 'Monday'
        elif self.week == 'Tuesday':
            return 'Tuesday'
        else:   
            return f"{self.week}s"
    
    def __str__(self):
        #return f"Schedule {self.schedule_id}: {self.train.name} - {self.start_date}-{self.end_date}, Week:{self.week
        return f"Schedule {self.schedule_id}: {self.train.train_name} - {self.start_date}"
